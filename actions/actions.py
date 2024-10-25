import logging
from typing import Any, Text, Dict, List
from rasa.core.actions import Action

# Thiết lập logger
logger = logging.getLogger(__name__)

class ActionHandleImage(Action):
    def name(self) -> Text:
        return "action_handle_image"

    async def run(
        self, dispatcher, tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Ghi log các sự kiện trong tracker
        logger.info(f"Tracker events: {tracker.events}")

        # Lấy dữ liệu từ message
        message = tracker.latest_message.get('text')
        if message is None:
            logger.error("Message is None. No data received.")
            dispatcher.utter_message(text="Không nhận được thông điệp.")
            return []

        # Ghi log message
        logger.info(f"Received message: {message}")

        # Lấy dữ liệu hình ảnh từ entities
        image_data = next(
            (entity.get("value") for entity in tracker.latest_message.get('entities', []) if entity.get("entity") == "image"),
            None
        )

        if image_data:
            logger.info(f"Received image data: {image_data}")

            # Kiểm tra xem image_data có chứa base64 hay không
            if "data:image/png;base64," in image_data:
                base64_image = image_data.split(",")[1]
                logger.info(f"Extracted base64 image data: {base64_image[:30]}...")  # Chỉ in ra một phần để tránh quá dài

                # Bạn có thể xử lý base64_image ở đây (lưu trữ, phân tích, ...)
                dispatcher.utter_message(text="Tôi đã nhận được hình ảnh từ bạn.")
            else:
                dispatcher.utter_message(text="Dữ liệu hình ảnh không hợp lệ.")
        else:
            dispatcher.utter_message(text="Không tìm thấy hình ảnh trong yêu cầu.")

        return []
from rasa_sdk import Action
from flask import request

class ActionAddHeader(Action):
    def name(self) -> str:
        return "action_add_header"

    async def run(self, dispatcher, tracker, domain):
        # Thêm header tùy chỉnh
        request.headers['ngrok-skip-browser-warning'] = 'true'
        # Tiếp tục xử lý yêu cầu
        return []
