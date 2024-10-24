from fastapi import APIRouter, HTTPException

import app.util.businessRuleUtil as psu
from app.model.models import StockDetailRequest
from app.util.bootStrapUtil import bootstrapper
from app.util.db import dbUtil

router = APIRouter()

@router.get("/status/")
async def get_status():
    return {
        "db_host": bootstrapper.db_name
    }

@router.post("/cross_tab_from_db/")
async def get_cross_tab_from_db(request: StockDetailRequest):

    selected_accounts = request.accounts
    selected_market = request.markets
    selected_stocks = request.stocks

    print("accounts --> ",selected_accounts )
    print("markets --> ", selected_market)
    print("stocks --> ", selected_stocks)

    stock_details_dict = await dbUtil.get_data_from_db()


    # Process the fetched data using cross_tab function
    if selected_accounts:
        result_df =  psu.create_crosstab (stock_details_dict,selected_accounts, selected_market, selected_stocks )
        print("----------------->",result_df.tail(5))
        result_json = result_df.to_json(orient='split')  # Convert DataFrame to JSON

        return {"cross_tab_result": result_json}
    else:
        raise HTTPException(status_code=404, detail="No data found")

