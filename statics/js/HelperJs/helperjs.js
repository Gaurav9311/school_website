var fileExtension = ['jpeg', 'jpg', 'png', 'gif', 'bmp'];
let monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

class Urls {
    static LogoutUrl = "/Login/Logout";
}

$(".table").children("tbody").children("tr").children("td").click(function() {
    $(".table").children("tbody").children("tr").removeClass("activeRow");
    $(this.parentNode).toggleClass("activeRow");
});

$(document).on('click', '.table tbody tr td', function(e) {
    $(".table").children("tbody").children("tr").removeClass("activeRow");
    $(this.parentNode).toggleClass("activeRow");
});
$(document).on('click', '#tableBody div.flex-table-item div.flex-table-cell', function() {
    $("#tableBody").children("div.flex-list-inner").children("div.flex-table-item").removeClass("activeRow");
    $(this.parentNode).toggleClass("activeRow");
});

let regExList = {
    alphaWithSymbols: new RegExp(/^[A-Za-z0-9_ -]+|[\.]|[\\]|[A-Za-z0-9_ -]+|[\.]+|[\\]+$/), // Alphanumeric with dash, underscore, fullstop and space
    alphaWithUrlSymbols: new RegExp(/^[A-Za-z0-9-_.]+$/), // Alphanumeric with dash, underscore, fullstop and space
    ifscValidation: new RegExp(/^([A-Z]{4}[0]{1}[A-Z0-9]{6})/), // ifsc Validation
    alphaWithSpace: new RegExp(/^[A-Za-z0-9 ]+$/), // AlphaNumeric With only space
    alphabetsOnly: new RegExp(/^[a-zA-Z ]+$/), // Alpha With only space
    emailKeys: new RegExp(/^[A-Za-z0-9@.-_]+$/), // AlphaNumeric With only space
    emailRegex: new RegExp(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/), // Email Regex
    numbersOnly: new RegExp(/^[0-9]+$/), // numbers Only
    time24formatOnly: new RegExp(/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/), // Time only 24 Hours format
    numberswithdashPlusOnly: new RegExp(/^[0-9-+]+$/), // numbers Only
    indianmobileOnly: new RegExp(/^[6-9]\d{9}$/), // indian mobile Only
    indianlandlineOnly: new RegExp(/^([0-9]{2,5}[-][0-9]{5,9})/), // indian landline number Only
    deciamlNumbersOnly: new RegExp(/^[0-9.]+$/), // numbers Only
    numberOnlyLimitTo100: new RegExp(/^[1-9][0-9]?$|^100$/), //percentage Validation
    numberOnly: new RegExp(/^[0-9]+$/), //number Only
    alphaNumericOnly: new RegExp(/^[A-Za-z0-9]+$/), // Alpha Numeric Only
    urlWithDashOnly: new RegExp(/^[A-Za-z0-9-]+$/), // Pattern to validate only url
    numberWithSpace: new RegExp(/^[0-9 ]+$/), // Pattern to validate numbers with space
    starRating: new RegExp(/^([1-4]{1}[.][0-9]{1})|([0]{1}[.][1-9]{1})|([5]{1}[.][0]{1})/),
    price: new RegExp(/^([1-9][.][0-9]{2})|([1-9])/),
    nonZeroValues: new RegExp(/^[1-9][0-9]*/),
    websiteUrl: new RegExp(/^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$/),
    facebookUrl: new RegExp(/^(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?/),
    emailPattern: new RegExp(/^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/)
};

function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
}

function toggleFieldReadonly($this, id) {
    if ($this.checked)
        $("#" + id).attr("readonly", false);
    else
        $("#" + id).attr("readonly", true);
}

function getPatternMessage(pattern) {
    switch (pattern) {
        case regExList.numbersOnly:
            return 'Numbers'
            break;
        case regExList.alphaWithSymbols:
            return 'Alphabets / Numbers'
            break;
        case regExList.alphaWithSpace:
            return 'Alphabets / Numbers with spaces'
            break;
        case regExList.emailRegex:
            return '@ symbol followed by valid domain name & (.)'
            break;
        case regExList.alphaWithUrlSymbols:
            return 'Alphabets and numbers with dash (-), dot(.) or underscore (_) are allowed.'
            break;
    }
}

function getInvalidKeysErrorMessage(pattern) {
    switch (pattern) {
        case regExList.numbersOnly:
            return 'Numbers are allowed'
            break;
        case regExList.alphaWithSymbols:
            return 'Alphabets and numbers with symbols are allowed'
            break;
        case regExList.alphaWithUrlSymbols:
            return 'Alphabets and numbers with symbols like Underscore(_), Dash(-), Dot(.) are allowed'
            break;
        case regExList.alphaWithSpace:
            return 'Only alphabets and numbers are allowed.'
            break;

    }
}

function getRequiredFieldErrorMessage(field) {
    return field.name + ' is required.';
}

function getPatternFieldErrorMessage(field, pattern) {
    return field.name + ' must contains ' + getPatternMessage(pattern);
}

function icheck(ClassName) {
    $().iCheck && $("." + ClassName).each(function() {
        var t = $(this).attr("data-checkbox") ? $(this).attr("data-checkbox") : "icheckbox_line-blue",
            e = $(this).attr("data-radio") ? $(this).attr("data-radio") : "iradio_line-blue";
        t.indexOf("_line") > -1 || e.indexOf("_line") > -1 ? $(this).iCheck({
            checkboxClass: t,
            radioClass: e,
            insert: '<div class="icheck_line-icon"></div>' + $(this).attr("data-label")
        }) : $(this).iCheck({
            checkboxClass: t,
            radioClass: e
        });
    });
}

function validateNumberKeys(e) {
    if ((e.keyCode > 47 && e.keyCode < 58) || (e.keyCode > 95 && e.keyCode < 105)) {
        return true;
    } else {
        return false;
    }
}

function validateUtilityKeys(e) {
    if (e.keyCode === 8 || e.keyCode === 9 || e.keyCode === 39 || e.keyCode === 37 || e.keyCode === 38 || e.keyCode === 40 || e.keyCode === 46) {
        return true;
    } else {
        return false;
    }
}

function validateUrlKeys(e) {
    if (e.keyCode !== 45 && (e.keyCode < 48 || (e.keyCode > 57 && e.keyCode < 65) || (e.keyCode > 90 && e.keyCode < 97) || e.keyCode > 122 && e.keyCode !== 45)) {
        return false;
    } else {
        return true;
    }
}

function validateAlphabetKeys(e) {
    if (e.keyCode > 64 && e.keyCode < 91) {
        return true;
    } else {
        return false;
    }
}

function imageExists(imageAddSpan, imageEditSpan, errorSpan, errorMessage) {
    if ($.inArray(imageEditSpan[0].src.split('.').pop().toLowerCase(), fileExtension) == -1) {
        if (imageAddSpan[0].files.length <= 0) {
            showImageError(imageAddSpan, errorSpan, errorMessage);
        } else {
            hideImageError(imageAddSpan, errorSpan);
        }
    }
}

function stopInvalidKeyPress(e, field, pattern) {
    if (!validateUtilityKeys(e)) {
        stopUnwantedKeys(e, field, pattern);
    }
}

function stopUnwantedKeys(e, inputField, regex) {

    if (!validateWithRegex(regex, e.key)) {
        e.preventDefault();
        $('#' + inputField.id).parent().addClass("has-error");
        $('#' + inputField.id).next("span").html(getInvalidKeysErrorMessage(regex));
        field.setCustomValidity(getInvalidKeysErrorMessage(regex));
    }
}

function stopUnwantedKeyPress(e, inputField, errorSpan, errorMessage, regex) {
    if (!validateWithRegex(regex, e.originalEvent.key)) {
        e.preventDefault();
        showError(inputField, errorSpan, errorMessage);
    }
}

function validateValues(e, inputField, errorSpan, errorMessage, regex) {
    if (!validateWithRegex(regex, inputField.val())) {
        e.preventDefault();
        showError(inputField, errorSpan, errorMessage);
    } else {
        hideError(inputField, errorSpan);
    }
}

function validateNonZero(e, inputField, errorSpan, errorMessage, regex) {
    if (!validateWithRegex(regex, inputField.val())) {
        e.preventDefault();
        showError(inputField, errorSpan, errorMessage);
    } else {
        hideError(inputField, errorSpan);
    }
}

function showError(inputField, errorSpan, errorMessage) {
    inputField.closest(".form-group").addClass("has-error");
    errorSpan.text(errorMessage);
}

function showImageError(inputField, errorSpan, errorMessage) {

    errorSpan.text(errorMessage);
    inputField.parent().parent().parent().parent().addClass("has-error");
}

function hideImageError(inputField, errorSpan) {
    errorSpan.text("");
    inputField.parent().parent().parent().parent().removeClass("has-error");
}

function hideError(inputField, errorSpan) {
    errorSpan.text("");
    inputField.closest(".form-group").removeClass("has-error");
}

function mandatoryIcheckValidation(checkboxClass, inputField, errorSpan, errorMessage) {

    if ($(checkboxClass + ':checked').length > 0) {
        hideIcheckError(checkboxClass, inputField, errorSpan);
    } else {
        showIcheckError(checkboxClass, inputField, errorSpan, errorMessage);
    }
}

function hideIcheckError(checkboxClass, inputField, errorSpan) {
    errorSpan.text("");
    $(checkboxClass).parent().removeClass('icheckbox_line-red_error').addClass('icheckbox_line-blue');
    inputField.closest(".form-group").removeClass("has-error");
}

function showIcheckError(checkboxClass, inputField, errorSpan, errorMessage) {
    inputField.closest(".form-group").addClass("has-error");
    $(checkboxClass).parent().removeClass('icheckbox_line-blue').addClass('icheckbox_line-red_error');
    errorSpan.text(errorMessage);
}

function mandatoryFieldValidation(inputField, errorSpan, errorMessage) {
    if (inputField.val().trim() !== "") {
        hideError(inputField, errorSpan);
    } else {
        showError(inputField, errorSpan, errorMessage);
    }
}

function mandatoryDropdownFieldValidation(inputField, errorSpan, errorMessage) {
    if (inputField.val().trim() == "" || inputField.val() == "0" || inputField.val() == 0 || inputField.val() == null) {
        showError(inputField, errorSpan, errorMessage);
    } else {
        hideError(inputField, errorSpan);
    }
}

function mandatoryFieldValidationForCkEditor(inputField, inputFieldValue, errorSpan, errorMessage) {
    if (inputFieldValue !== "") {
        hideError(inputField, errorSpan);
    } else {
        showError(inputField, errorSpan, errorMessage);
    }
}

function reloadPage() {
    setTimeout(function() {
        window.location.reload()
    }, 1000);
}

function validateFutureTime(dateValue, timeValue, errorSpan, errorMessage) {
    var dd = dateValue.val().split('/')[0];
    var mm = dateValue.val().split('/')[1];
    var yy = dateValue.val().split('/')[2];
    var hh = timeValue.val().split(':')[0];
    var MM = timeValue.val().split(':')[1];
    var startDateValue = new Date(yy, mm, dd, hh, MM, 00, 00);
    var todaysDate = new Date();
    if (startDateValue < todaysDate) {
        showError(timeValue, errorSpan, errorMessage);
        eError(timeValue, errorSpan);
    } else {
        hideError(timeValue, errorSpan);
    }
}

function validateStartTimeEndTimeWithOutDate(startTime, endTime, errorSpan, errorMessage) {
    var dd = getCurrentDate().split('/')[0];
    var mm = getCurrentDate().split('/')[1];
    var yy = getCurrentDate().split('/')[2];
    var edd = getCurrentDate().split('/')[0];
    var emm = getCurrentDate().split('/')[1];
    var eyy = getCurrentDate().split('/')[2];
    var shh = startTime.val().split(':')[0];
    var sMM = startTime.val().split(':')[1];
    var ehh = endTime.val().split(':')[0];
    var eMM = endTime.val().split(':')[1];
    var startDateValue = new Date(yy, mm, dd, shh, sMM, 00, 00);
    var endDateValue = new Date(eyy, emm, edd, ehh, eMM, 00, 00);
    if (startDateValue < endDateValue) {
        hideError(endTime, errorSpan);
    } else {
        showError(endTime, errorSpan, errorMessage);
    }
}

function validateStartTimeEndTime(startDate, startTime, endDate, endTime, errorSpan, errorMessage) {
    var dd = startDate.val().split('/')[0];
    var mm = startDate.val().split('/')[1];
    var yy = startDate.val().split('/')[2];
    var edd = endDate.val().split('/')[0];
    var emm = endDate.val().split('/')[1];
    var eyy = endDate.val().split('/')[2];
    var shh = startTime.val().split(':')[0];
    var sMM = startTime.val().split(':')[1];
    var ehh = endTime.val().split(':')[0];
    var eMM = endTime.val().split(':')[1];
    var startDateValue = new Date(yy, mm, dd, shh, sMM, 00, 00);
    var endDateValue = new Date(eyy, emm, edd, ehh, eMM, 00, 00);
    if (startDateValue < endDateValue) {
        hideError(endTime, errorSpan);
    } else {
        showError(endTime, errorSpan, errorMessage);
    }
}

function validateFutureDates(dateValue, errorSpan, errorMessage) {
    var dd = dateValue.val().split('/')[0];
    var mm = dateValue.val().split('/')[1];
    var yy = dateValue.val().split('/')[2];
    var date = new Date(yy, mm, dd, 00, 00, 00, 00);
    var todaysDate = new Date();
    if (date > todaysDate) {
        hideError(dateValue, errorSpan);
    } else {
        showError(dateValue, errorSpan, errorMessage);
    }
}

function validatePastDates(dateValue, errorSpan, errorMessage) {
    var dd = dateValue.val().split('/')[0];
    var mm = dateValue.val().split('/')[1];
    var yy = dateValue.val().split('/')[2];
    var date = new Date(yy, mm, dd, 00, 00, 00, 00);
    var todaysDate = new Date();
    if (date < todaysDate) {
        hideError(dateValue, errorSpan);
    } else {
        showError(dateValue, errorSpan, errorMessage);
    }
}

//validate Start Date and end Date
function validateStartDateEndDate(startDate, endDate, errorSpan, errorMessage) {
    var dd = startDate.val().split('/')[0];
    var mm = startDate.val().split('/')[1];
    var yy = startDate.val().split('/')[2];
    var startDateValue = new Date(yy, mm, dd, 00, 00, 00, 00);
    var edd = endDate.val().split('/')[0];
    var emm = endDate.val().split('/')[1];
    var eyy = endDate.val().split('/')[2];
    var endDateValue = new Date(eyy, emm, edd, 00, 00, 00, 00);
    if (startDateValue > endDateValue) {
        showError(endDate, errorSpan, errorMessage);
    } else {
        hideError(endDate, errorSpan);
    }
}

//validate total and available quantities
function compareTwoNumberInputs(data1, data2) {
    if (parseInt(data1) > parseInt(data2)) return false;
    else return true;
}

// Get Current Date
function getCurrentDate() {
    var fullDate = new Date();
    var twoDigitMonth = (parseInt(fullDate.getMonth()) + 1).toString(); + "";
    if (twoDigitMonth.length === 1) twoDigitMonth = "0" + twoDigitMonth;
    var twoDigitDate = fullDate.getDate() + "";
    if (twoDigitDate.length === 1) twoDigitDate = "0" + twoDigitDate;
    var currentDate = twoDigitDate + "/" + twoDigitMonth + "/" + fullDate.getFullYear();
    return currentDate;
}

// Get Current Date after days
function getDateAfterDays(days) {
    var fullDate = new Date();
    fullDate.setDate(fullDate.getDate() + days);
    var twoDigitMonth = (parseInt(fullDate.getMonth()) + 1).toString(); + "";
    if (twoDigitMonth.length === 1) twoDigitMonth = "0" + twoDigitMonth;
    var twoDigitDate = fullDate.getDate() + "";
    if (twoDigitDate.length === 1) twoDigitDate = "0" + twoDigitDate;
    var currentDate = twoDigitDate + "/" + twoDigitMonth + "/" + fullDate.getFullYear();
    return currentDate;
}

// Get Current Date after month
function getDateAfterMonths(months) {
    var fullDate = new Date();
    fullDate.setDate(fullDate.getMonth() + months);
    var twoDigitMonth = (parseInt(fullDate.getMonth()) + 1).toString(); + "";
    if (twoDigitMonth.length === 1) twoDigitMonth = "0" + twoDigitMonth;
    var twoDigitDate = fullDate.getDate() + "";
    if (twoDigitDate.length === 1) twoDigitDate = "0" + twoDigitDate;
    var currentDate = twoDigitDate + "/" + twoDigitMonth + "/" + fullDate.getFullYear();
    return currentDate;
}

function reloadPage() {
    setTimeout(function() {
        window.location.reload()
    }, 1000);
}

function validateWithRegex(pattern, data) {

    if (data && pattern) {

        if (pattern.test(data)) {
            return true;
        } else {
            return false;
        }
    } else {
        return true;
    }
}

function matchWithRegex(pattern, data) {
    if (data && pattern) {
        if (data.match(pattern)) {
            return true;
        } else {
            return false;
        }
    } else {
        return true;
    }
}

function populateUrlAsName(NameFieldId, UrlFieldId) {
    UrlFieldId.val(NameFieldId.val().replace(/[^a-zA-Z0-9 -]/g, "").replace(/\s\s+/g, ' ').replace(/ /g, "-").replace(/-+/g, '-')
        .toLowerCase());
}

function populateFieldSameAsAnotherField(fieldId, fieldId2) {
    fieldId2.val(fieldId.val());
}

function populateUrlAsNameNew(NameFieldId, UrlFieldId) {
    UrlFieldId.value = NameFieldId.value.trim().replace(/[^a-zA-Z0-9 -]/g, "").replace(/\s\s+/g, ' ').replace(/ /g, "-").replace(/-+/g, '-').toLowerCase();
}

function populateFieldSameAsAnotherFieldNew(fieldId, fieldId2) {
    fieldId2.value = fieldId.value;
}

function populateCanonicalUrl(fieldId, fieldId2, domainName) {
    fieldId2.value = domainName + fieldId.value.trim().replace(/[^a-zA-Z0-9 -]/g, "").replace(/\s\s+/g, ' ').replace(/ /g, "-").replace(/-+/g, '-').toLowerCase();
}

function ChangeDateFormatToDDMMMMYYYY(date) {
    var newdate = new Date(date);
    var dateDay = appendLeadingZeroes(newdate.getDate());
    var dateMonth = monthNames[newdate.getMonth()];
    var dateYear = newdate.getFullYear();
    return `${dateDay}-${dateMonth}-${dateYear}`;
}

function appendLeadingZeroes(n) {
    if (n <= 9) {
        return "0" + n;
    }
    return n
}
async function BindPartialPageWithAnimation($this, Url, Options) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    $this.fadeOut(500, function() {
        $this.html(Response).show();
    });
}

async function BindDropDown($this, Url, Options, SelectedData, IsErrorDisplay) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    if (Response.responseModel.isSuccess) {
        var data = Response.responseModel.data;
        var items = '';
        items += "<option value=''>" + "Please select" + "</option>";
        $this.empty();
        $.each(data, function(i, DropDownList) {
            items += "<option value='" + DropDownList.value + "'>" + DropDownList.text + "</option>";
        });
        $this.html(items);
        if (parseInt(SelectedData) != 0) {
            $this.val(parseInt(SelectedData));
        }
    } else if (IsErrorDisplay)
        toastr.error(Response.responseModel.errorMessage);

}

async function BindDropDownWithDynamicFirstOption($this, Url, Options, SelectedData, IsErrorDisplay, Content) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    if (Response.responseModel.isSuccess) {
        var data = Response.responseModel.data;
        var items = '';
        items += "<option value='0'> " + Content + " </option>";
        $this.empty();
        $.each(data, function(i, DropDownList) {
            items += "<option value='" + DropDownList.value + "'>" + DropDownList.text + "</option>";
        });
        $this.html(items);
        if (parseInt(SelectedData) != 0) {
            $this.val(SelectedData);
        }
    } else if (IsErrorDisplay)
        toastr.error(Response.responseModel.errorMessage);
}

async function BindDropDownWithFirstSelectedOption($this, Url, Options, SelectedData, IsErrorDisplay) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    if (Response.responseModel.isSuccess) {
        var data = Response.responseModel.data;
        var items = '';
        $this.empty();
        $.each(data, function(i, DropDownList) {
            if (i == 0) {
                items += "<option selected value='" + DropDownList.value + "'>" + DropDownList.text + "</option>";
            } else {
                items += "<option value='" + DropDownList.value + "'>" + DropDownList.text + "</option>";
            }
        });
        $this.html(items);
        if (parseInt(SelectedData) != 0) {
            $this.val(SelectedData);
        }
    } else if (IsErrorDisplay)
        toastr.error(Response.responseModel.errorMessage);

}



async function BindMultiSelectRemoveDropDown($this, Url, Options, SelectedData, IsErrorDisplay) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    if (Response.responseModel.isSuccess) {
        debugger;
        var data = Response.responseModel.data;
        var items = '';
        items += "<option disabled value='" + "" + "'>" + "Please select" + "</option>";
        /*items += "<option value='" + "selectAll" + "'>" + "Select All" + "</option>";*/
        $this.empty();
        $.each(data, function(i, DropDownList) {
            items += "<option value='" + DropDownList.value + "'>" + DropDownList.text + "</option>";
        });
        $this.html(items);
        if (SelectedData != "") {
            var List = SelectedData.split(',');
            $this.val(List);
        }
    } else if (IsErrorDisplay)
        toastr.error(Response.responseModel.errorMessage);
}

async function BindMultiSelectDropDown($this, Url, Options, SelectedData, IsErrorDisplay, Content) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    if (Response.responseModel.isSuccess) {
        var data = Response.responseModel.data;
        var items = '';
        items += "<option value='' disabled='disabled'>" + Content + "</option>";
        $this.empty();
        $.each(data, function(i, DropDownList) {
            items += "<option value='" + DropDownList.value + "'>" + DropDownList.text + "</option>";
        });
        $this.html(items);
        if (SelectedData != "") {
            var List = SelectedData.split(',');
            $this.val(List);
        }
    } else if (IsErrorDisplay) {
        $this.empty();
        $this.append("<option value='' disabled='disabled'>" + Response.responseModel.errorMessage + "</option>");
        toastr.error(Response.responseModel.errorMessage);
    } else {
        $this.empty();
        $this.append("<option value='' disabled='disabled'>No Data Found</option>");
    }
}

async function BindPartialPage($this, Url, Options) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    $this.empty();
    $this.html(Response);
}

async function BindPartialDataTablePage($this, Url, Options, IsReorder) {
    var Response = await AjaxCallWithResponse(Url, Options, "get");
    $this.empty();
    $this.html(Response);
    $this.DataTable().destroy();
    if (IsReorder) {
        $this.DataTable({
            rowReorder: true
        });
    } else
        $this.DataTable();
}
(function($) {
    $.fn.multiSelectr = function(options) {
        if (typeof options === 'string') {
            var args = Array.prototype.slice.call(arguments, 1);

            return this.each(function() {
                var instance = $(this).data('multiSelectr');

                if (instance && typeof instance[options] === 'function') {
                    instance[options].apply(instance, args);
                }
            });
        }
        return this.each(function() {
            var $this = $(this);
            var instance = $this.data('multiSelectr');

            if (!instance) {
                // Create a new instance if not already exists
                instance = new MultiSelectr(this, options);
                $this.data('multiSelectr', instance);
            }
        });
    };

    function MultiSelectr(element, options) {
        this.$element = $(element);
        this.ddlClassSelector = new Selectr(element, options);

        var selectedValues = Array.from(element.options)
            .filter(option => option.selected)
            .map(option => option.value);
        this.ddlClassSelector.setValue(selectedValues);

        this.isSelectAll = false;
        this.valuesToSelect = [];
        var self = this;
        this.ddlClassSelector.on('selectr.change', function() {
            self.onChange();
        });
        this.ddlClassSelector.on('selectr.close', function() {
            self.onClose();
        });

        this.onClose = function() {
            setTimeout(function() {
                if (typeof self.closeCallback === 'function') {
                    var selectedData = self.ddlClassSelector.getValue();
                    self.closeCallback(selectedData);
                }

                if (self.ddlClassSelector.placeEl) {
                    self.ddlClassSelector.placeEl.classList.remove('parsley-error');
                }
                if (self.ddlClassSelector.container) {
                    const element = self.ddlClassSelector.container.querySelector('.parsley-errors-list');
                    if (element) {
                        element.remove();
                    }
                }
                if (self.ddlClassSelector.el) {
                    self.ddlClassSelector.el.classList.remove('parsley-error');
                }
                if (self.ddlClassSelector.selected) {
                    self.ddlClassSelector.selected.style.backgroundColor = '#fff';
                }
            }, 50);
        };


        this.onChange = function() {
            var selectedValues = self.ddlClassSelector.getValue();
            if (selectedValues.includes('selectAll') && !self.isSelectAll) {
                self.isSelectAll = true;
                var allOptions = Array.from(self.ddlClassSelector.options);
                var allValues = allOptions.map(option => option.value);
                self.valuesToSelect = allValues.filter(value => value !== '');
                self.ddlClassSelector.setValue(self.valuesToSelect);
            } else if (!selectedValues.includes('selectAll') && self.isSelectAll) {
                self.isSelectAll = false;
                if (selectedValues.length == 0 || selectedValues.length == self.valuesToSelect.length - 1) {
                    self.valuesToSelect = [];
                    self.ddlClassSelector.setValue([]);
                } else {
                    self.valuesToSelect = selectedValues.filter(value => value !== '');
                    self.ddlClassSelector.setValue(self.valuesToSelect);
                }
                self.ddlClassSelector.close();
            } else {
                self.valuesToSelect = selectedValues;
            }
            if (typeof self.changeCallback === 'function') {
                self.changeCallback(self.ddlClassSelector.getValue());
            }
        };

        this.getSelectedValues = function() {
            return self.ddlClassSelector.getValue();
        };


        // Public method to set the change callback
        this.setChangeCallback = function(callback) {
            if (typeof callback === 'function') {
                self.changeCallback = callback;
            }
        };


        this.setCloseCallback = function(callback) {
            if (typeof callback === 'function') {
                self.closeCallback = callback;
            }
        };

        this.destroy = function() {
            if (self.ddlClassSelector) {
                self.ddlClassSelector.destroy();
            }
            // Clean up any other resources if needed
            self.$element.removeData('multiSelectr');
        };

        this.disable = function() {
            if (self.ddlClassSelector) {
                self.ddlClassSelector.disable();
                if (self.ddlClassSelector.placeEl) {
                    self.ddlClassSelector.placeEl.classList.remove('parsley-error');
                }
                if (self.ddlClassSelector.container) {
                    const element = self.ddlClassSelector.container.querySelector('.parsley-errors-list');
                    if (element) {
                        element.remove();
                    }
                }
                if (self.ddlClassSelector.el) {
                    self.ddlClassSelector.el.classList.remove('parsley-error');
                }
                if (self.ddlClassSelector.selected) {
                    self.ddlClassSelector.selected.style.backgroundColor = '#fff';
                }
            }
        };

        // Public method to enable the instance
        this.enable = function() {
            if (self.ddlClassSelector) {
                self.ddlClassSelector.enable();
                if (self.ddlClassSelector.placeEl) {
                    self.ddlClassSelector.placeEl.classList.remove('parsley-error');
                }
                if (self.ddlClassSelector.container) {
                    const element = self.ddlClassSelector.container.querySelector('.parsley-errors-list');
                    if (element) {
                        element.remove();
                    }
                }
                if (self.ddlClassSelector.el) {
                    self.ddlClassSelector.el.classList.remove('parsley-error');
                }
                if (self.ddlClassSelector.selected) {
                    self.ddlClassSelector.selected.style.backgroundColor = '#fff';
                }
            }
        };
        this.$element.trigger('change');
    }
})(jQuery);

function btnloading(element, isEnabled) {
    if (isEnabled)
        $("#" + element.id).addClass('is-loading');
    else
        setTimeout(function() {
            $("#" + element.id).removeClass('is-loading');
        }, 1500);

}

async function DeleteData(Url, Id, ButtonText = "Delete") {
    initConfirm(ButtonText + ' box', "Are you sure? You won't be able to revert this!.", false, false, ButtonText, 'Cancel', async function(closeEvent) {
        var Options = {
            Id: parseInt(Id)
        }
        await AjaxCallWithNotification(Url, Options, "post");
    });
}

async function DeleteDataWithDynamicMessage(Url, Id, Message, ButtonText = "Delete") {
    initConfirm(ButtonText + ' box', Message, false, false, ButtonText, 'Cancel', async function(closeEvent) {
        var Options = {
            Id: parseInt(Id)
        }
        await AjaxCallWithNotification(Url, Options, "post");
    });
}

async function DeleteDataWithRedirect(Url, Id, RedirectUrl, ButtonText = "Delete") {
    initConfirm(ButtonText + ' box', "Are you sure? You won't be able to revert this!.", false, false, ButtonText, 'Cancel', async function(closeEvent) {
        var Options = {
            Id: parseInt(Id)
        }
        await AjaxCallWithNotificationAndRedirect(Url, Options, "post", RedirectUrl);
    });
}

async function ResetPassword(Url, Id, Type) {
    initConfirm('Reset Password box', "Are you sure? You won't be able to revert this!.", false, false, 'Reset Password', 'Cancel', async function(closeEvent) {
        var Options = {
            Id: parseInt(Id),
            UserType: parseInt(Type)
        }
        await AjaxCallWithNotification(Url, Options, "post");
    });
}

function GenerateSerialNumber(count) {
    return count++;
}

function EditButton(EditLink) {
    return '<a href="' + EditLink + '" class="button is-primary is-circle is-elevated"><span class="icon is-small"><i data-feather="edit"></i></span></a>'
}

function DeleteButton(EditLink) {
    return '<a onclick="DeleteData(' + EditLink + ')" class="button is-danger is-circle is-elevated"><span class="icon is-small"><i data-feather="trash"></i></span></a>'
}

async function ToggleForMapping(Url, $this, FirstField, SecondField) {
    var Options = {
        FirstField: parseInt(FirstField),
        SecondField: parseInt(SecondField),
        IsSelected: $this.checked
    }
    await AjaxCallWithNotification(Url, Options, "post");
}