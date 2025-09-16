import uuid
from datetime import timedelta
from contextlib import contextmanager
import pymssql
import jdatetime
from services.setting import settings


@contextmanager
def db_connection():
    conn = pymssql.connect(
        host=settings.SMS_DB_HOST,
        user=settings.SMS_DB_USER,
        password=settings.SMS_DB_PASSWORD,
        database=settings.SMS_DB_NAME,
    )
    try:
        yield conn
    finally:
        conn.close()

def current_jalali_datetime():
    now = jdatetime.datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%H:%M")
    datetime_str = f"{date_str}-{time_str}"
    return date_str, time_str, datetime_str

def send_sms_alert(message: str, record: int = 0):
    
    DEFAULT_MOBILE_NOS = ["*********", "*********"]
    DEFAULT_TABLE_NAME = "TABLE_NAME"
    DEFAULT_SMS_TYPE = 13
    
    date_str, time_str, datetime_str = current_jalali_datetime()
    date_part, time_part = datetime_str.split('-')
    jdt = jdatetime.datetime.strptime(f"{date_part} {time_part}", "%Y/%m/%d %H:%M")
    new_jdt = jdatetime.datetime.fromgregorian(datetime=jdt.togregorian() + timedelta(hours=1))
    new_datetime_str = new_jdt.strftime("%Y/%m/%d-%H:%M:%S")

    sms_data = {
        "Id": str(uuid.uuid4()),
        "Message": message,
        "Comment": "",
        "Param1": "",
        "Param2": "",
        "ParamCount": 0,
        "MobileNo": None,
        "MessageKey": None,
        "OldMessageKey": None,
        "InSending": False,
        "CreateDateTime": datetime_str,
        "HasExpaired": False,
        "IsSuccessful": False,
        "EntityUniqueInfo": record,
        "RelatedEntityId": record,
        "RelatedTableName": DEFAULT_TABLE_NAME,
        "Status": None,
        "ExpirationDate": new_datetime_str,
        "CheckStatusDateTime": "",
        "TemplateName": "",
        "SmsType": DEFAULT_SMS_TYPE,
        "RequestUserId": None,
        "IsSendToServerOutbox": False,
        "SendDateTime": datetime_str
    }

    with db_connection() as conn, conn.cursor() as cursor:
        for mobile_no in DEFAULT_MOBILE_NOS:
            sms_data = sms_data.copy()
            sms_data.update({
                "Id": str(uuid.uuid4()),
                "MobileNo": mobile_no,
            })

            columns = ", ".join(sms_data.keys())
            placeholders = ", ".join(["%s"] * len(sms_data))
            sql = f"INSERT INTO SmsOutbox ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, tuple(sms_data.values()))
                conn.commit()
                print(f"[Success] Inserted SMS record for {mobile_no}")
            except Exception as e:
                print(f"[Error] SMS insert failed for {mobile_no}: {e}")