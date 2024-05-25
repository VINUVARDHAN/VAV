var baseURL = null;
var appDetails = null;
var companyDetails =  null;
function setCommonDetailsFromHiddenValues(){
    if(baseURL==null){
        var hiddenValues = $("#hidden_values");
        baseURL = hiddenValues.find("#baseURL").val();
        appDetails = JSON.parse(hiddenValues.find("#appDetails").val().replace(/'/g, '"'));
        companyDetails =  JSON.parse(hiddenValues.find("#companyDetails").val().replace(/'/g, '"'));
    }
}
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
alertUtils = {
    showAlert : function showAlert(message, duration,type) {
        var id = $("#message_display");
        id.html("<b><p>"+message+"</p></b>");
        id.css("display", "block");
        if(type=='error'){
            id.css("color", "red");
        }else if (type=='success'){
            id.css("color", "green");
        }else{
            id.css("color", "black");
        }
        alertTimeout = setTimeout(function() {
            id.css("display", "none");
        }, duration);
    },

    startLoadingAnimation : function() {
        var loadingBar = document.getElementById('loading-bar');
        loadingBar.style.height = '5px';
    },

    stopLoadingAnimation: function() {
        var loadingBar = document.getElementById('loading-bar');
        loadingBar.style.height = '0'; 
    }
}
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
clientUtil = {
    redirectPage : function(response){
        if(response.redirectURL!=undefined){
            alertUtils.showAlert(response.success.name,3000,'error');
            setTimeout(function() {
                window.location.href = response.redirectURL;
            }, 3000);
        }
    },
    openTab : function(tabName) {
        var tabIds = ["expense_records","create_and_edit_page","complete_report"];
        for (var i = 0; i < tabIds.length; i++) {
            $("#" + tabIds[i]).css("display", "none");
            $('#head_'+tabIds[i]).removeClass("selected_tab_head");
            $('#head_' + tabIds[i]).addClass("tab_head_buttons");
        }    
        $('#head_' + tabName).removeClass("tab_head_buttons");
        $('#head_' + tabName).addClass("selected_tab_head");
        $("#"+tabName).css("display", "block");
    },
    getCreatePage : function(){
        $("#edit_page").css("display", "none");
        clientUtil.openTab("create_and_edit_page");
        $("#create_page").css("display", "block");
    },
    getEditPageById : async function(id) {
        var requestDetails = {
            "requestPayLoad" : {
                "id" : id,
            },
            "method" : 'GET',
            "uri" : appDetails.apiName+'/Records/'
        }
        var responseDetails = await clientUtil.makeCallToServer(requestDetails);
        if(responseDetails.isSuccess){
            $("#create_page").css("display", "none");
            $("#edit_page").html(responseDetails.response.data.html);
            $("#edit_page").css("display", "block");
            clientUtil.openTab("create_and_edit_page");
        }else{
            alertUtils.showAlert(responseDetails.response.responseJSON.error,5000,'error');
        }
    },
    downloadHtml : function(id) {
        const element = document.getElementById(id);
        html2canvas(element, {
            logging: false, // Disable logging to console
            scrollY: -window.scrollY, // Set scroll position to top
            useCORS: true, // Enable CORS to capture cross-origin images
            scale: 2, // Increase scale for better resolution (optional)
            onrendered: function(canvas) {
                const pdfWidth = 8.27; // Width of A4 page in inches
                const pdfHeight = 11.69; // Height of A4 page in inches
                const scale = Math.min(pdfWidth / canvas.width, pdfHeight / canvas.height);
                const pdf = new jsPDF('p', 'in', [pdfWidth, pdfHeight]);
                pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, canvas.width * scale, canvas.height * scale);
                pdf.save("document.pdf");
            }
        });
    },
    makeCallToServer : async function(requestDetails){
        alertUtils.startLoadingAnimation();
        return new Promise(function(resolve, reject) {
            $.ajax({
                url: baseURL + '/' + companyDetails.apiName + '/' + requestDetails.uri,
                type: requestDetails.method,
                dataType: 'json',
                data: requestDetails.requestPayLoad==undefined?null:requestDetails.requestPayLoad,
                headers: requestDetails.headers,
                success: function (response) {
                    clientUtil.redirectPage(response);
                    resolve( { "isSuccess" : true , "response" : response} );
                    alertUtils.stopLoadingAnimation();
                },
                error: function (xhr) {
                    resolve( { "isSuccess" : false , "response" : xhr} );
                    alertUtils.stopLoadingAnimation();
                }
            });
        });
    }
}
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
recordUtil = {
    getRecords : async function(page,count) {
        var requestDetails = {
            "requestPayLoad" : {
                "page" : page,
                "count" : count
            },
            "method" : 'GET',
            "uri" : appDetails.apiName+'/Records/'
        }
        var responseDetails = await clientUtil.makeCallToServer(requestDetails);
        if(responseDetails.isSuccess){
            $("#expense_records").html(responseDetails.response.data.html);
        }else{
            alertUtils.showAlert(responseDetails.response.responseJSON.error,5000,'error');
        }
    },

    deleteRecord : async function(id){
        var catergoryName = $("#record_"+id).find("#record_category_name_"+id)[0].dataset["categoryName"];
        var additionalInfo = $("#record_"+id).find("#record_additional_info_"+id)[0].dataset["additionalInfo"];
        additionalInfo = additionalInfo!=""?additionalInfo:"---";
        var amount = $("#record_"+id).find("#record_amount_"+id)[0].dataset["amount"];
        var date = $("#record_"+id).find("#record_date_"+id)[0].dataset["date"];
        var message = "Are you sure you want to delete this record? "+catergoryName+" : "+additionalInfo+" : "+amount+" : "+date;
        var deleteConfirmed = await confirm(message);
        if(deleteConfirmed){
            var requestDetails = {
                "requestPayLoad" : JSON.stringify({
                    "id" : id,
                }),
                "method" : 'DELETE',
                "uri" : appDetails.apiName+'/Records/'
            }
            var responseDetails = await clientUtil.makeCallToServer(requestDetails);
            if(responseDetails.isSuccess){
                alertUtils.showAlert(responseDetails.response.success.name,2000,'success');
                recordUtil.getRecords(1,document.getElementById('count_per_page').value);
            }else{
                alertUtils.showAlert(responseDetails.response.responseJSON.error,5000,'error');
            }
        }
    },

    addRecord : async function(){
        $("#create_save").css("display", "none");
        var fields = ["categoryId", "additional_info", "amount", "date"]
        var fieldsIds = ["category_id_create", "additional_info_create", "amount_create", "date_create"]
        var data = {}
        for(var i=0;i<fields.length;i++){
            data[fields[i]] = $("#" + fieldsIds[i])[0].value;
        }
        var requestDetails = {
            "requestPayLoad" : JSON.stringify(data),
            "method" : 'POST',
            "uri" : appDetails.apiName+"/Records/",
            "headers" : {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        }
        var responseDetails = await clientUtil.makeCallToServer(requestDetails);
        if(responseDetails.isSuccess){
            recordUtil.completeReport();
            alertUtils.showAlert(responseDetails.response.success.name,2000,'success');
            recordUtil.getRecords(1,$("#count_per_page")[0].value);
            for(var i=0;i<fields.length;i++){
                $("#" + fieldsIds[i]).val("");
            }
        }else{
            alertUtils.showAlert(responseDetails.response.responseJSON.error,5000,'error');
        }
        $("#create_save").css("display", "block");
    },

    editRecord : async function(id) {
        $("#edit_save").css("display", "none");
        var isDiffFound = false;
        var newData = {};
        var fields = ["categoryId", "additional_info", "amount", "date"];
        var fieldIds = ["category_id","additional_info","amount","date"]
        for (var i = 0; i < fieldIds.length; i++) {
            var valueAfter = $("#edit_" + fieldIds[i])[0].value;
            var valueBefore = $("#edit_" + fieldIds[i])[0].dataset[fields[i]];
            if (valueAfter!=valueBefore) {
                isDiffFound = true;
                newData[fields[i]] = valueAfter;
            }
        }
        if (isDiffFound) {
            var requestDetails = {
                "requestPayLoad" : JSON.stringify(newData),
                "method" : 'PUT',
                "uri" : appDetails.apiName+"/Records/?id=" + id,
                "headers" : {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            }
            var responseDetails = await clientUtil.makeCallToServer(requestDetails);
            if(responseDetails.isSuccess){
                recordUtil.completeReport();
                var recordElement = $("#record_" + id);
                var $categoryIcon = $(responseDetails.response.data.category_image);
                if (recordElement.length !== 0) { // Check if the element exists
                    recordElement.find("#record_amount_" + id).text(responseDetails.response.data.amount);
                    recordElement.find("#record_category_name_" + id).text(responseDetails.response.data.category_name +" ").append($categoryIcon);
                    recordElement.find("#record_additional_info_" + id).text(responseDetails.response.data.additional_info);
                    recordElement.find("#record_date_" + id).text(responseDetails.response.data.date);
                }
                alertUtils.showAlert(responseDetails.response.success.name,2000,'success');
                clientUtil.openTab("expense_records");
            }else{
                alertUtils.showAlert(responseDetails.response.responseJSON.error,5000,'error');
            }
        }else{
            alertUtils.showAlert("No difference found to save changes in Record",2000);
        }
        $("#edit_save").css("display", "block");
    },

    onCountChange : function(element){
        recordUtil.getRecords(1,element.value);
    },
    completeReport : async function() {
        var requestDetails = {
            "method" : 'GET',
            "uri" : appDetails.apiName+"/Records/CompleteReport"
        }
        var responseDetails = await clientUtil.makeCallToServer(requestDetails);
        if(responseDetails.isSuccess){
            $("#complete_report").html(responseDetails.response.data.html);
        }else{
            alertUtils.showAlert(responseDetails.response.responseJSON.error,5000,'error');
        }
    }
}

//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("create_form").addEventListener("submit", function(event) {
        event.preventDefault();
        if (this.checkValidity()) {
            recordUtil.addRecord();
        } else {
            console.log("Form validation failed.");
        }
    });
});

//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function logout(){
    var requestDetails = {
        "method" : 'GET',
        "uri" : "Logout/"
    }
    var responseDetails = await clientUtil.makeCallToServer(requestDetails);
    if(responseDetails.isSuccess){
        clientUtil.redirectPage(responseDetails);
    }
}
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 