import uuid
def processRefund(refundRequest):
    #Refund Processing
    orderNumber = refundRequest['orderNumber']
    refundID = uuid.uuid4()
    return f"Refund For {orderNumber} processed successfully. Refund Reference {refundID}"

def processReturn(returnRequest):
    orderNumber = returnRequest['orderNumber']
    returnID = uuid.uuid4()
    return f"Return For {orderNumber} initiated successfully. Return Reference {returnID}"
nofunctionsArr = []
functionsArr = [
        {
            "name": "processRefund",
            "description": "Processes Refund for an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "orderNumber": {
                        "type": "string",
                        "description": "Order Number needed for refund"
                    },
                    "customername": {
                        "type": "string",
                        "description": "Name of the customer"
                    }

                },
                "required": ["orderNumber", "customername"]
            },


        },
        {
            "name": "processReturn",
            "description": "Processes Return for an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "orderNumber": {
                        "type": "string",
                        "description": "Order Number needed for return"
                    },
                    "customername": {
                        "type": "string",
                        "description": "Name of the customer"
                    }

                },
                "required": ["orderNumber", "customername"]
            },

        },

    ]