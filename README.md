# Flask API Server

Serve project data for visualization

## Notes

+ `git pull` to update local files on cloud server from origin
+ `wsgi.py` should have `import app from app`, since app is initialized there
+ edit request path before deployment
  + `http://localhost:5001/api/dRidgeline?start_date=${start_date}&end_date=${end_date}`
  + `/api/dRidgeline?start_date=${start_date}&end_date=${end_date}`
