import azure.functions as func
import logging
from filter_services import apply_filter_to_image

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def parse_request(req: func.HttpRequest) -> FilterRequest:
    filter_type = req.form.get('filter')
    image_file = req.files.get('image')
    
    if not filter_type or not image_file:
        raise ValueError("Missing filter or image")
    
    try:
        return FilterRequest(filter=filter_type, image_data=image_file)
    except ValidationError as e:
        raise ValueError(f"Invalid request: {e}")

@app.route(route="apply_filter")
def apply_filter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Parse and validate the request using the Pydantic model
        filter_request = parse_request(req)
        
        filtered_image_data = apply_filter_to_image(
            filter_request.image_data, 
            filter_request.filter
        )

        return func.HttpResponse(
            filtered_image_data,
            status_code=200,
            mimetype='image/jpeg'  # Adjust mimetype if needed
        )

    except ValueError as e:
        return func.HttpResponse(str(e), status_code=400)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse("An internal server error occurred", status_code=500)





@app.route(route="default")
def default(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )