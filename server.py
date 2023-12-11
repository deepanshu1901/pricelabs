from fastapi import FastAPI, Query, HTTPException, Response
from vrboAPI import main, getDates, process_csv

app = FastAPI()

# @app.get("/")
# def get_all_properties():
#     return main()

# @app.get("/filtered-properties")
# def get_properties_filtered_by_distance(distance: float = Query(..., description="Filter properties by distance"), destination: str = Query(..., description="Destination")):
#     try:
#         # Attempt to convert the distance parameter to float
#         distance = float(distance)
#     except ValueError:
#         # If conversion fails, raise an HTTPException with a 422 Unprocessable Entity status code
#         raise HTTPException(status_code=422, detail="Invalid distance parameter. Must be a valid float.")
#     return main(radius=distance, destination=destination)
@app.get("/top-price-for-property")
def get_top_price_for_property(property_id: str = Query(..., description="Filter properties by distance")):
    pass

@app.get("/properties-by-date")
def get_properties_filtered_by_distance(distance: float = Query(..., description="Filter properties by distance"), destination: str = Query(..., description="Destination")):
    try:
        # Attempt to convert the distance parameter to float
        distance = float(distance)
    except ValueError:
        # If conversion fails, raise an HTTPException with a 422 Unprocessable Entity status code
        raise HTTPException(status_code=422, detail="Invalid distance parameter. Must be a valid float.")
    
    headers = {
        "Content-Disposition": "attachment; filename=data.csv",
        "Content-Type": "text/csv",
    }

    df = getDates()
    csv_content = process_csv(df)

    # Return the CSV file as a Response
    return Response(content=csv_content, media_type="text/csv", headers=headers)

@app.get("/health")
def health():
    return {"status": "ok"}