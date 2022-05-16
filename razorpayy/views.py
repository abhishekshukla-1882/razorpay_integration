from django.shortcuts import render

# Create your views here.
import razorpay
# print('jhfgsdfgsjgfjsd')




# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=("rzp_test_qJq7FOICRHV1dU", "GJC5XMcMSoYXVBBmYXipeYCN"))
 
 
def homepage(request):
    currency = 'INR'
    amount = 50000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = "rzp_test_qJq7FOICRHV1dU"
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'index.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
# @csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 50000  # Rs. 200
                try:
 
                    razorpay_client.payment.capture(payment_id, amount)
 
                    return render(request, 'paymentsuccess.html')
                except:
 
                    return render(request, 'paymentfail.html')
            else:
 
                return render(request, 'paymentfail.html')
        except:
 
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()