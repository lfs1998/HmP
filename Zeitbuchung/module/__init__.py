from flask import Flask

app = Flask( __name__ )
app.config[ "SECRET_KEY" ] = "1f451998dcdbc80097b88d39cc201077"

from module import routes
from module import database

print("Pakete wurden geladen!")