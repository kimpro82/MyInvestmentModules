# Download Stock Price Data with tidyquant
# 2023.06.17


# 필요한 라이브러리를 로드합니다
if (!requireNamespace("tidyquant")) {
    install.packages("tidyquant")
}
library(tidyquant)

# 작업 디렉토리를 설정합니다. 해당 경로에 저장될 것입니다.
setwd({path})

# 다운로드 받을 종목의 심볼을 정의합니다
symbols <- c("122630.KS", "252670.KS")  # KODEX 레버리지, KODEX 200선물인버스2X

# 데이터를 다운로드할 기간을 설정합니다
start_date <- "2022-01-01"
end_date <- "2022-12-31"

# 종목 데이터를 다운로드합니다
data <- tq_get(symbols, from = start_date, to = end_date)
head(data)
str(data)

# 데이터프레임을 CSV 파일로 저장합니다
current_datetime <- format(Sys.time(), "%Y%m%d_%H%M%S")
write.csv(data, file = paste0("stock_data_", current_datetime, ".csv"))
