import os

class Config:
    DEBUG=bool(os.environ.get('DEBUG', 'False'))
    ENV=os.environ.get('ENV', 'production')
    HOST=os.environ.get('HOST', '0.0.0.0')
    PORT=os.environ.get('PORT', '5000')