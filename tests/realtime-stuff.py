import requests
import time
import logging
from typing import Optional, Dict, Any, Callable
from dotenv import load_dotenv
import os
from datetime import datetime
import json

# Load environment variables
load_dotenv()

class RealtimeDataCollector:
    """
    A class for collecting real-time data from APIs with robust error handling,
    rate limiting, and state management.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: str = "",
                 update_interval: float = 1.0,
                 max_retries: int = 3,
                 timeout: int = 10):
        """
        Initialize the data collector.
        
        Args:
            api_key: API key for authentication (will try to get from env if None)
            base_url: Base URL for the API
            update_interval: Seconds between data requests
            max_retries: Maximum number of retry attempts on failure
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.getenv('API_KEY')
        self.base_url = base_url or os.getenv('API_BASE_URL', '')
        self.update_interval = update_interval
        self.max_retries = max_retries
        self.timeout = timeout
        
        # State management
        self.is_running = False
        self.last_update = None
        self.error_count = 0
        self.total_requests = 0
        self.data_history = []
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}' if self.api_key else '',
            'User-Agent': 'RealtimeDataCollector/1.0'
        })
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Callback functions
        self.on_data_received: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def set_callbacks(self, 
                     on_data: Optional[Callable] = None,
                     on_error: Optional[Callable] = None):
        """Set callback functions for data reception and error handling."""
        self.on_data_received = on_data
        self.on_error = on_error
    
    def fetch_data(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict]:
        """
        Fetch data from a specific endpoint.
        
        Args:
            endpoint: API endpoint to call
            params: Additional parameters for the request
            
        Returns:
            JSON response data or None if failed
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.max_retries + 1):
            try:
                self.logger.debug(f"Fetching data from {url} (attempt {attempt + 1})")
                
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                
                data = response.json()
                self.last_update = datetime.now()
                self.total_requests += 1
                self.error_count = 0  # Reset error count on success
                
                return data
                
            except requests.exceptions.RequestException as e:
                self.error_count += 1
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"Max retries exceeded for {url}")
                    if self.on_error:
                        self.on_error(e)
                    return None
            
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON response: {e}")
                if self.on_error:
                    self.on_error(e)
                return None
    
    def start_realtime_collection(self, 
                                endpoint: str,
                                params: Dict[str, Any] = None,
                                store_history: bool = True,
                                max_history_size: int = 1000):
        """
        Start real-time data collection.
        
        Args:
            endpoint: API endpoint to monitor
            params: Parameters for the API call
            store_history: Whether to store data history
            max_history_size: Maximum number of historical records to keep
        """
        self.is_running = True
        self.logger.info(f"Starting real-time data collection from {endpoint}")
        
        try:
            while self.is_running:
                start_time = time.time()
                
                # Fetch new data
                data = self.fetch_data(endpoint, params)
                
                if data:
                    # Store in history if enabled
                    if store_history:
                        self.data_history.append({
                            'timestamp': datetime.now().isoformat(),
                            'data': data
                        })
                        
                        # Limit history size
                        if len(self.data_history) > max_history_size:
                            self.data_history = self.data_history[-max_history_size:]
                    
                    # Call data callback
                    if self.on_data_received:
                        self.on_data_received(data)
                    
                    self.logger.info(f"Data updated at {self.last_update}")
                
                # Calculate sleep time to maintain consistent intervals
                elapsed_time = time.time() - start_time
                sleep_time = max(0, self.update_interval - elapsed_time)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            self.logger.info("Collection stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in collection loop: {e}")
            if self.on_error:
                self.on_error(e)
        finally:
            self.stop()
    
    def stop(self):
        """Stop real-time data collection."""
        self.is_running = False
        self.session.close()
        self.logger.info("Data collection stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        return {
            'is_running': self.is_running,
            'total_requests': self.total_requests,
            'error_count': self.error_count,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'history_size': len(self.data_history)
        }
    
    def export_history(self, filename: str):
        """Export data history to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.data_history, f, indent=2)
        self.logger.info(f"History exported to {filename}")


# Example usage
def main():
    """Example usage of the RealtimeDataCollector."""
    
    # Create collector instance
    collector = RealtimeDataCollector(
        base_url=os.getenv('API_BASE_URL', 'https://api.example.com'),
        update_interval=5.0,  # 5 seconds between requests
        max_retries=3
    )
    
    # Define callback functions
    def handle_new_data(data):
        print(f"New data received: {json.dumps(data, indent=2)}")
        # Process your data here
        
    def handle_error(error):
        print(f"Error occurred: {error}")
        # Handle errors (logging, alerts, etc.)
    
    # Set callbacks
    collector.set_callbacks(
        on_data=handle_new_data,
        on_error=handle_error
    )
    
    try:
        # Start collecting data
        collector.start_realtime_collection(
            endpoint='your-endpoint',
            params={'param1': 'value1'},
            store_history=True
        )
    finally:
        # Export data before closing
        collector.export_history('data_history.json')
        print("Final stats:", collector.get_stats())


if __name__ == "__main__":
    main()