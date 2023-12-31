from fastapi import FastAPI, Query, HTTPException, Response
from vrboAPI import main, getPrices, get_top_prices, RESULT_FILE

app = FastAPI()

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

    csv_content = getPrices(destination=destination, radius=distance).to_csv(index=False)

    # Return the CSV file as a Response
    return Response(content=csv_content, media_type="text/csv", headers=headers)  
    
@app.get("/get-top-prices")
def get_top_prices_of_properties(destination: str = Query(..., description="Destination"), radius: float = Query(..., description="Radius")):

    # if RESULT_FILE does not exist, or is empty, or contains only the header, then run the main function
    df = getPrices(destination=destination, radius=radius)

    headers = {
        "Content-Disposition": "attachment; filename=data.csv",
        "Content-Type": "text/csv",
    }

    csv_content = get_top_prices(df).to_csv(index=False)

    # Return the CSV file as a Response
    return Response(content=csv_content, media_type="text/csv", headers=headers)

@app.get("/health")
def health():
    return {"status": "ok"}