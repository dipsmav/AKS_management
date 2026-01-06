#!/usr/bin/env python
"""
AKS Management Dashboard - Application Entry Point
"""
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import MOCK_MODE directly from config
from app.config import MOCK_MODE


def setup_logging(debug: bool = False):
    """Setup logging to console and file"""
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # File handler - always logs everything
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    return log_file


def main():
    """Main entry point for the application"""
    from app import create_app, socketio
    
    # Get configuration
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5050))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    # Setup logging
    log_file = setup_logging(debug)
    logger = logging.getLogger('run')
    
    # Determine mode from config.py (not environment)
    mode_str = 'MOCK (Testing)' if MOCK_MODE else 'PRODUCTION (Real kubectl)'
    
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║           AKS Management Dashboard                            ║
╠═══════════════════════════════════════════════════════════════╣
║   Mode: {mode_str:<45}║
║   Host: {host}:{port:<50}║
║   Debug: {str(debug):<44}║
║   Logs: {str(log_file):<45}║
╠═══════════════════════════════════════════════════════════════╣
║   Open http://localhost:{port} in your browser                 ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    logger.info(f"Starting AKS Management Dashboard")
    logger.info(f"MOCK_MODE = {MOCK_MODE}")
    logger.info(f"Log file: {log_file}")
    
    if not MOCK_MODE:
        logger.info("Production mode - will use real kubectl commands")
        import subprocess
        import platform
        from app.config import Config
        from app.services.env_utils import get_subprocess_env
        
        is_windows = platform.system() == 'Windows'
        
        # Get environment with CLI paths from config
        env = get_subprocess_env()
        
        # Log configured paths
        if Config.KUBECTL_PATH:
            logger.info(f"Custom kubectl path configured: {Config.KUBECTL_PATH}")
        if Config.AZURE_CLI_PATHS:
            logger.info(f"Azure CLI search paths: {Config.AZURE_CLI_PATHS}")
        
        # Verify kubectl is available
        try:
            result = subprocess.run(['kubectl', 'version', '--client'], 
                                   capture_output=True, text=True, timeout=5,
                                   shell=is_windows, env=env)
            if result.returncode == 0:
                version_line = result.stdout.strip().split('\n')[0]
                logger.info(f"kubectl found: {version_line}")
            else:
                logger.warning(f"kubectl check failed: {result.stderr}")
        except FileNotFoundError:
            logger.error("kubectl NOT FOUND - please install kubectl")
        except Exception as e:
            logger.error(f"kubectl check error: {e}")
        
        # Verify az cli is available
        try:
            result = subprocess.run(['az', '--version'], 
                                   capture_output=True, text=True, timeout=10,
                                   shell=is_windows, env=env)
            if result.returncode == 0:
                az_version = result.stdout.strip().split('\n')[0]
                logger.info(f"Azure CLI found: {az_version}")
            else:
                logger.warning(f"az cli check failed: {result.stderr}")
        except FileNotFoundError:
            logger.error("Azure CLI NOT FOUND - please install az cli")
        except Exception as e:
            logger.error(f"az cli check error: {e}")
    
    # Create the application
    app = create_app()
    
    # Run with SocketIO support
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        allow_unsafe_werkzeug=debug  # Only allow in debug mode
    )


if __name__ == '__main__':
    main()
