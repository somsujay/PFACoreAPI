from fastapi import APIRouter, HTTPException

import app.service.stockSummaryUtil as psu
from app.model.models import StockDetailRequest
from app.util.bootStrapUtil import bootstrapper
from app.util.loggingUtil import logger as lgr

router = APIRouter()

@router.get("/status/")
async def get_status():
    return {
        "db_host": bootstrapper.db_name
    }

@router.post("/get_stock_details/")
async def get_stock_details(request: StockDetailRequest):

    selected_accounts = request.accounts
    selected_market = request.markets
    selected_stocks = request.stocks

    lgr.info(f"accounts : {selected_accounts}")
    lgr.info(f"markets : {selected_market}")
    lgr.info(f"stocks : {selected_stocks}")

    # Process the fetched data using cross_tab function
    if selected_accounts:
        result_df =  await psu.getAccWiseStocksDetails (selected_accounts, selected_market, selected_stocks)
        #print("----------------->",result_df.tail(5))
        result_json = result_df.to_json(orient='split')  # Convert DataFrame to JSON

        return {"cross_tab_result": result_json}
    else:
        raise HTTPException(status_code=404, detail="No data found")

