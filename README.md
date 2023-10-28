# Welcome to our Payment Service Solution

Things that you need in order to test the payment systems:
- For Stripe you can use one of the 3 provided test cards:
 4000000000009995 - Failed payment
 4000002500003155 - Requires authentication (3D)
 4242424242424242 - Successful payment
 use date in the future like 12/34
 any 3 numbers as CVC

- For Coinbase (there is no sandbox there) you need real crypto in order to make
successful payment.

All test API keys are saved in settings.py
