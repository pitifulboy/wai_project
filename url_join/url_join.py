
param = ('1', '000001', '2023-03-21', '2023-03-28', '5', '5b98e82a71a2afd3b84c5d14ad192c57', 'all')

MinuteKLine_url = "http://api.waizaowang.com/doc/getMinuteKLine?" \
                  "type=%s&code=%s&startDate=%s&endDate=%s&export=%s&token=%s&fields=%s" \
                  % param

print(MinuteKLine_url)
