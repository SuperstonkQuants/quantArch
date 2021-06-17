
from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.oci.devops import APIService
from diagrams.aws.analytics import Glue, GlueCrawlers, GlueDataCatalog, Athena, EMR
from diagrams.custom import Custom
from diagrams.onprem.client import Users, User
from diagrams.aws.network import ELB



ftp_icon = "img/ftp.png"
cloudflare = "img/cf.png"


with Diagram("Datalake", show=False):

    with Cluster("                API Data Sources                "):
        fintel       = APIService("Fintel")
        quandl       = APIService("Quandl")
        finra        = APIService("FINRA")
        alphavantage = APIService("Alpha Vantage")
        binance      = APIService("Binance")
        coinmarket   = APIService("CoinMarketCap API")
        degiro       = APIService("Degiro API")
        fred         = APIService("FRED")
        fmp          = APIService("Financial Modeling Prep")
        finhub       = APIService("Finhub")
        oanda        = APIService("Oanda")
        polygon      = APIService("Polygon")
        tradier      = APIService("Tradier")
        orats        = APIService("Orats")
        iex          = APIService("IEX")
        others       = APIService("Others...")

    with Cluster("                FTP Data Sources                "):
        nyseFtp  = Custom("NYSE", ftp_icon)
        oratsFtp = Custom("Orats", ftp_icon)

    with Cluster("                Ingest Lambdas                "):
        fintelIngest      = Lambda("Fintel Ingest")
        quandlIngest      = Lambda("Quandl Ingest")
        finraIngest       = Lambda("FINRA Ingest")
        alphavantageIngest= Lambda("Alpha Vantage Ingest")
        binanceIngest     = Lambda("Binance Ingest")
        coinmarketIngest  = Lambda("CoinMarketCap \r    API Ingest")
        degiroIngest      = Lambda("Degiro API Ingest")
        fredIngest        = Lambda("FRED Ingest")
        fmpIngest         = Lambda("FMP Ingest")
        finhubIngest      = Lambda("Finhub Ingest")
        oandaIngest       = Lambda("Oanda Ingest")
        polygonIngest     = Lambda("Polygon Ingest")
        tradierIngest     = Lambda("Tradier Ingest")
        oratsIngest       = Lambda("Orats Ingest")
        iexIngest         = Lambda("IEX Ingest")
        othersIngest      = Lambda("Others...")
        nyseFtpIngest     = Lambda("NYSE FTP Ingest")
        oratsFtpIngest    = Lambda("Orats FTP Ingest")
   
    rawObjectStore = S3("S3 IngestLake")

    with Cluster("Data Processing"):
        etlObjectStore = S3("S3 DataLake")

        with Cluster("Data Catalog"):
            glueCrawler = GlueCrawlers("Glue ETL Jobs")
            glueDataCatalog = GlueDataCatalog("Glue Data Catalog")
            glueETL = Glue("Glue ETL")
        
        with Cluster("Analytics"):
            athena = Athena("Athena SQL")
            emr = EMR("Map Reduce")

    with Cluster("Analyzed Data"):
        processedData = S3("Output Data")

    datascientists = Users("DataScience")

    lb = ELB("lb")
    public = Users("Public access")
    cf = Custom("Cloudflare", cloudflare)
    svc_group = Lambda("Web Render")


    nyseFtp      >> nyseFtpIngest      >> rawObjectStore
    oratsFtp     >> oratsFtpIngest     >> rawObjectStore
    fintel       >> fintelIngest       >> rawObjectStore
    quandl       >> quandlIngest       >> rawObjectStore
    finra        >> finraIngest        >> rawObjectStore
    alphavantage >> alphavantageIngest >> rawObjectStore
    binance      >> binanceIngest      >> rawObjectStore
    coinmarket   >> coinmarketIngest   >> rawObjectStore
    degiro       >> degiroIngest       >> rawObjectStore
    fred         >> fredIngest         >> rawObjectStore
    fmp          >> fmpIngest          >> rawObjectStore
    finhub       >> finhubIngest       >> rawObjectStore
    oanda        >> oandaIngest        >> rawObjectStore
    polygon      >> polygonIngest      >> rawObjectStore
    tradier      >> tradierIngest      >> rawObjectStore
    orats        >> oratsIngest        >> rawObjectStore
    iex          >> iexIngest          >> rawObjectStore
    others       >> othersIngest       >> rawObjectStore

    rawObjectStore >> glueCrawler >> glueDataCatalog >> glueETL >> glueDataCatalog
    glueETL >> etlObjectStore
    etlObjectStore >> athena
    glueDataCatalog >> athena
    etlObjectStore >> emr
    glueDataCatalog >> emr
    emr >> processedData
    athena >> processedData
    datascientists << athena
    datascientists << processedData
    datascientists >> processedData 

    public << cf << lb << svc_group << processedData

