from website import create_app

app = create_app()
# App will run only if we run exactly THIS file
if __name__ == "__main__":
        app.run(debug=True)

        

