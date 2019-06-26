#coding=utf-8
# saving urls
APP_VERSION="1.4.9"

BASIC_ACCOUNT_URL = "https://account.onethingpcs.com/"
LOGIN_URL = BASIC_ACCOUNT_URL+"user/login?appversion={0}".format(APP_VERSION)
CHECK_SESSION_URL = BASIC_ACCOUNT_URL+"user/check-session?appversion={0}".format(APP_VERSION)

ACCOUNT_INFO_URL = BASIC_ACCOUNT_URL + "wkb/account-info"
ACTIVE_USER_INFO_URL = BASIC_ACCOUNT_URL + "activate/userinfo?appversion={0}".format(APP_VERSION)

WKB_INCOME_URL = BASIC_ACCOUNT_URL + "wkb/income-history"
WKB_OUTCOME_URL = BASIC_ACCOUNT_URL + "wkb/outcome-history"

BASIC_CONTROL_URL = "https://control.onethingpcs.com/"
LIST_PEER_URL = BASIC_CONTROL_URL + "listPeer?"
PEER_USB_INFO_URL = BASIC_CONTROL_URL + "getUSBInfo?"

BASIC_REMOTEDL_URL = "https://control.remotedl.onethingpcs.com/"
LIST_REMOTE_DOWNLOAD_LIST_URL = BASIC_REMOTEDL_URL+"list?"
CREATE_REMOTE_DOWNLOAD_TASK_URL = BASIC_REMOTEDL_URL+"createTask?"
CREATE_REMOTE_BT_DOWNLOAD_TASK_URL = BASIC_REMOTEDL_URL+"createBtTask?"
LOGIN_REMOTE_DOWNLOAD_URL = BASIC_REMOTEDL_URL+"login?"
URLRESOLVE_REMOTE_DOWNLOAD_URL = BASIC_REMOTEDL_URL+"urlResolve?"
