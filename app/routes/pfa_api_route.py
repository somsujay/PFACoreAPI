import json

import orjson
from fastapi import APIRouter, HTTPException

import app.service.stockSummaryUtil as psu
from app.model.models import StockDetailRequest, MarketWsStockRequest
from app.util.bootstrap_util import bootstrapper
from app.util.logging_util import logger as lgr

router = APIRouter()

@router.get("/status/")
async def get_status():
    return {
        "db_host": bootstrapper.db_name,
        "env_type": bootstrapper.env_type,
        "env_name": bootstrapper.env_name
    }

@router.post("/get_stock_details/")
async def get_stock_details(request: StockDetailRequest):

    selected_accounts = request.accounts
    selected_market = request.markets
    selected_stocks = request.stocks

    lgr.info(f"accounts : {selected_accounts} markets : {selected_market} stocks : {selected_stocks}")

    # Process the fetched data using cross_tab function
    if selected_accounts:
        acc_wise_stocks_details_df =  await psu.get_acc_wise_stocks_details (selected_accounts, selected_market, selected_stocks)
        lgr.debug(f" Final Result Returned : {acc_wise_stocks_details_df.tail(5)}")
        acc_wise_stocks_details_json = acc_wise_stocks_details_df.to_json(orient='records')  # Convert DataFrame to JSON

        return {"acc_ws_stocks_details": acc_wise_stocks_details_json}
    else:
        raise HTTPException(status_code=404, detail="No data found")


@router.post("/get_market_ws_stocks/")
async def get_market_ws_stock(request: MarketWsStockRequest):

    try:
        selected_accounts = request.accounts
        selected_market = request.markets

        lgr.info(f"accounts : {selected_accounts} markets : {selected_market}")

        # Process the fetched data using cross_tab function
        if selected_accounts:
            market_wise_stocks =  await psu.get_market_wise_stocks (selected_accounts, selected_market)

            #lgr.info(f" Final Result Returned : {market_wise_stocks}")

            market_wise_stocks_json = orjson.dumps(market_wise_stocks, default=str).decode("utf-8")  # Convert Decimals to strings or floats

            #market_wise_stocks_json = json.dumps(market_wise_stocks)  # Convert DataFrame to JSON

            lgr.debug(f" Final Result Returned : {market_wise_stocks_json}")

            return {"market_wise_stocks": market_wise_stocks_json}
        else:
            raise HTTPException(status_code=404, detail="No data found")
    except Exception as e:
        lgr.error('Error Getting Data from Database....%s', e)
        raise e
