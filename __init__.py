from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db
import random
from operator import itemgetter
from datetime import datetime, date

from allUsers import *
from viewPoints import *
from redemptionInfo import *
from redemptionHistory import *
from redemptionProductInfo import *

cred = credentials.Certificate("key.json")
firebase_config = {
  "databaseURL": "https://appsecprojbettina-default-rtdb.asia-southeast1.firebasedatabase.app/"
}
firebase_admin.initialize_app(cred, firebase_config)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    ref = db.reference()
    subchild_ref = ref.child("allUsers").child("TayAngeline")
    redemptionStatus = subchild_ref.child("redemptionStatus").get()

    if redemptionStatus is not None:
        subchild_ref.child("redemptionStatus").delete()

    return render_template("index.html", redemptionStatus=redemptionStatus)

@app.route("/viewpoints", methods=["GET","POST"])
def viewpoints():
    ref = db.reference()
    subchild_ref = ref.child("allUsers").child("TayAngeline").child("pointInfo")
    userPointsGet = subchild_ref.get()
    points = userPointsGet["points"]
    expiryDateStr = userPointsGet["expiryDate"]

    expireDays = None

    if points == 0 and expiryDateStr != "noDate":
        viewPoints1 = viewPoints()
        viewPoints1.set_expiryDate("noDate")
        subchild_ref.set(viewPoints1.to_dict())

    elif points != 0 and expiryDateStr != "noDate":
        expiryDate = datetime.strptime(expiryDateStr, "%d/%m/%Y")
        expireDays = (expiryDate - datetime.now()).days + 1

        if expireDays <= 0:
            viewPoints1 = viewPoints()
            viewPoints1.set_points(0)
            viewPoints1.set_expiryDate("noDate")
            subchild_ref.set(viewPoints1.to_dict())
            return redirect(url_for("viewpoints"))

    return render_template("viewpoints.html", points=points, expiryDateStr=expiryDateStr, expireDays=expireDays)



@app.route("/redemption", methods=["GET","POST"])
def redemption():
    ref = db.reference()

    #product information
    redemptionProductInfoGet = ref.child("redemptionProductInfo").get()
    redemptionProductName = redemptionProductInfoGet["redemptionProductName"]
    redemptionProductCost = redemptionProductInfoGet["redemptionProductCost"]
    redemptionProductRetail = redemptionProductInfoGet["redemptionProductRetail"]
    redemptionProductDescription = redemptionProductInfoGet["redemptionProductDescription"]

    #functions
    subchild_ref = ref.child("allUsers").child("TayAngeline").child("pointInfo")
    userPointsGet = subchild_ref.get()
    points = userPointsGet["points"]

    if request.method == "POST":
        quantity = int(request.form.get("quantity"))

        if quantity * int(redemptionProductCost) > points:
            return redirect(url_for("redemption"))

        redemptionInfo1 = redemptionInfo()
        redemptionInfo1.set_quantity(quantity)
        ref.child("allUsers").child("TayAngeline").child("redemptionInfo").set(redemptionInfo1.to_dict())

        return redirect(url_for("redemptioncheckout"))

    return render_template("redemption.html", redemptionProductName=redemptionProductName, redemptionProductCost=redemptionProductCost, redemptionProductRetail=redemptionProductRetail, redemptionProductDescription=redemptionProductDescription, points=points)

@app.route("/redemptioncheckout", methods=["GET","POST"])
def redemptioncheckout():
    ref = db.reference()

    subchild_ref1 = ref.child("allUsers").child("TayAngeline")
    userInfoGet = subchild_ref1.get()
    fName = userInfoGet["fName"]
    lName = userInfoGet["lName"]
    email = userInfoGet["email"]
    address = userInfoGet["address"]
    pcode = userInfoGet["pcode"]

    subchild_ref2 = ref.child("allUsers").child("TayAngeline").child("redemptionInfo")
    redemptionInfoGet = subchild_ref2.get()
    quantity = redemptionInfoGet["quantity"]

    subchild_ref3 = ref.child("redemptionProductInfo")
    redemptionProductInfoGet = subchild_ref3.get()
    redemptionProductName = redemptionProductInfoGet["redemptionProductName"]
    redemptionProductCost = redemptionProductInfoGet["redemptionProductCost"]

    tPoints = int(quantity) * int(redemptionProductCost)

    if request.method == "POST":
        dAddress = request.form.get("dAddress")
        dpCode = request.form.get("dpCode")

        redemptionInfo1 = redemptionInfo()
        redemptionInfo1.set_quantity(quantity)
        redemptionInfo1.set_dAddress(dAddress)
        redemptionInfo1.set_dpCode(dpCode)
        redemptionInfo1.set_otp(random.randint(100000, 999999))

        subchild_ref2.set(redemptionInfo1.to_dict())

        return redirect(url_for("otpverification"))

    return render_template("redemptioncheckout.html", fName=fName, lName=lName, email=email, address=address, pcode=pcode, quantity=quantity, redemptionProductName=redemptionProductName, redemptionProductCost=redemptionProductCost, tPoints=tPoints)

@app.route("/otpverification", methods=["GET","POST"])
def otpverification():
    ref = db.reference()

    subchild_ref1 = ref.child("allUsers").child("TayAngeline")
    userInfoGet = subchild_ref1.get()
    fName = userInfoGet["fName"]
    lName = userInfoGet["lName"]
    email = userInfoGet["email"]

    subchild_ref2 = ref.child("allUsers").child("TayAngeline").child("redemptionInfo")
    redemptionInfoGet = subchild_ref2.get()
    quantity = redemptionInfoGet["quantity"]
    dAddress = redemptionInfoGet["dAddress"]
    dpCode = redemptionInfoGet["dpCode"]
    otp = redemptionInfoGet["otp"]

    subchild_ref3 = ref.child("redemptionProductInfo")
    redemptionProductInfoGet = subchild_ref3.get()
    redemptionProductName = redemptionProductInfoGet["redemptionProductName"]
    redemptionProductCost = redemptionProductInfoGet["redemptionProductCost"]

    tPoints = int(quantity) * int(redemptionProductCost)

    if request.method == "POST":
        matchotp = int(request.form.get("matchotp"))
        if otp == matchotp:
            subchild_ref4 = ref.child("allUsers").child("TayAngeline").child("pointInfo")
            pointInfoGet = subchild_ref4.get()
            points = pointInfoGet["points"]
            updatedPoints = points - tPoints
            subchild_ref4.update({"points": updatedPoints})

            orderid = "Order " + str(random.randint(1000, 9999))

            redemptionHistory1 = redemptionHistory()
            redemptionHistory1.set_itemName(redemptionProductName)
            redemptionHistory1.set_itemQuantity(quantity)
            redemptionHistory1.set_itemCost(int(quantity)*int(redemptionProductCost))
            redemptionHistory1.set_redemptionDate(datetime.now().strftime("%d/%m/%Y"))
            redemptionHistory1.set_dAddress(dAddress)
            redemptionHistory1.set_redemptionDateTime(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            ref.child("allUsers").child("TayAngeline").child("orderHistory").child(orderid).set(redemptionHistory1.to_dict())

            subchild_ref2.delete()

            redemptionStatus = "Redemption successful!"
            ref.child("allUsers").child("TayAngeline").child("redemptionStatus").set(redemptionStatus)

            return redirect(url_for("index"))

        else:
            subchild_ref2.delete()

            redemptionStatus = "OTP incorrect, redemption unsuccessful."
            ref.child("allUsers").child("TayAngeline").child("redemptionStatus").set(redemptionStatus)

            return redirect(url_for("index"))

    return render_template("otpverification.html", fName=fName, lName=lName, email=email, dAddress=dAddress, dpCode=dpCode, quantity=quantity, redemptionProductName=redemptionProductName, redemptionProductCost=redemptionProductCost, tPoints=tPoints)

@app.route("/redemptionhistory", methods=["GET", "POST"])
def redemptionhistory():
    ref = db.reference()
    subchild_ref1 = ref.child("allUsers").child("TayAngeline").child("orderHistory")
    orderHistory = subchild_ref1.get()

    searchTerm = request.args.get("search", "")

    if not orderHistory:
        return render_template("redemptionhistory.html", orderHistoryEmpty=True, searchTerm=searchTerm, showLink=False)

    filteredOrders = []
    for orderid, order in orderHistory.items():
        itemName = order["itemName"]
        if searchTerm.lower() in itemName.lower():
            filteredOrders.append({
                "orderid": orderid,
                "itemName": itemName,
                "itemQuantity": order["itemQuantity"],
                "itemCost": order["itemCost"],
                "redemptionDate": order["redemptionDate"],
                "dAddress": order["dAddress"],
                "redemptionDateTime": order["redemptionDateTime"]
            })

    if not filteredOrders:
        return render_template("redemptionHistory.html", filteredOrders=None, searchTerm=searchTerm, showLink=False)

    sortedOrders = sorted(filteredOrders, key=itemgetter("redemptionDateTime"), reverse=True)

    tableRows = []
    for order in sortedOrders:
        tableRow = {
            "orderid": order["orderid"],
            "itemName": order["itemName"],
            "itemQuantity": order["itemQuantity"],
            "itemCost": order["itemCost"],
            "redemptionDate": order["redemptionDate"],
            "dAddress": order["dAddress"]
        }
        tableRows.append(tableRow)

    showLink = bool(searchTerm)
    return render_template("redemptionhistory.html", tableRows=tableRows, filteredOrders=filteredOrders, searchTerm=searchTerm, showLink=showLink)

@app.route("/redemptionproductupdate", methods=["GET", "POST"])
def redemptionproductupdate():
    redemptionUpdated = False

    ref = db.reference()

    if request.method == "POST":
        redemptionProductName = request.form.get("redemptionProductName")
        redemptionProductCost = request.form.get("redemptionProductCost")
        redemptionProductRetail = request.form.get("redemptionProductRetail")
        redemptionProductDescription = request.form.get("redemptionProductDescription").replace('\n', '<br>')
        redemptionProductImage = request.files["redemptionProductImage"]

        redemptionProductInfo1 = redemptionProductInfo()
        redemptionProductInfo1.set_redemptionProductName(redemptionProductName)
        redemptionProductInfo1.set_redemptionProductCost(redemptionProductCost)
        redemptionProductInfo1.set_redemptionProductRetail(redemptionProductRetail)
        redemptionProductInfo1.set_redemptionProductDescription(redemptionProductDescription)
        redemptionProductInfo1.saveRedemptionProductImage(redemptionProductImage)
        ref.child("redemptionProductInfo").set(redemptionProductInfo1.to_dict())

        redemptionUpdated = True

        return render_template("redemptionproductupdate.html", redemptionUpdated=redemptionUpdated)

    return render_template("redemptionproductupdate.html", redemptionUpdated=redemptionUpdated)


def setUsers():
    ref = db.reference("allUsers")
    user1 = allUsers()
    user1.set_fName("Tay")
    user1.set_lName("Angeline")
    user1.set_email("chickenpie30@gmail.com")
    user1.set_address("Yishun Street 123")
    user1.set_pcode("567321")
    ref.child(user1.get_fName() + user1.get_lName()).set(user1.to_dict())

    ref = db.reference("allUsers")
    user2 = allUsers()
    user2.set_fName("Ang")
    user2.set_lName("Bettina")
    user2.set_email("nudegets@gmail.com")
    user2.set_address("Bishan Street 123")
    user2.set_pcode("567123")
    ref.child(user2.get_fName() + user2.get_lName()).set(user2.to_dict())

    pointInfo1 = viewPoints()
    pointInfo1.set_points(500)
    pointInfo1.set_expiryDate("23/07/2023")
    ref.child(user1.get_fName() + user1.get_lName()).child("pointInfo").set(pointInfo1.to_dict())

    pointInfo2 = viewPoints()
    pointInfo2.set_points(200)
    ref.child(user2.get_fName() + user2.get_lName()).child("pointInfo").set(pointInfo2.to_dict())

if __name__ == "__main__":
    app.run()


