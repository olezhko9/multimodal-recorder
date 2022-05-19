import traceback

from flask import Blueprint, request, jsonify, Response
from service import device_service


def get_device_api(device_manager):
    router = Blueprint('device_router', __name__)

    @router.route("/devices")
    def get_devices():
        res = device_service.get_devices()
        return jsonify(res)

    @router.route('/device/start', methods=['POST'])
    def start_device():
        try:
            devices = request.json
            if type(devices) is not list:
                devices = [devices]

            for device in devices:
                device_id = device['device_id']

                if device_manager.get_device(device_id) is not None:
                    continue

                device_params = {}
                if device.get('settings'):
                    for param in device['settings']:
                        device_params[param['name']] = param['value']

                device_manager.add_and_run_device(device_id, device_params)
                device_manager.read_data()
        except Exception:
            traceback.print_exc()
            device_manager.stop_and_remove_devices()
            return "Error when trying connect to device", 500

        return jsonify(True)

    @router.route('/device/stop', methods=['POST'])
    def stop_device():
        try:
            devices = request.json
            if type(devices) is not list:
                devices = [devices]

            for device in devices:
                device_id = device['device_id']
                device_manager.stop_and_remove_device(device_id)
        except:
            traceback.print_exc()
            return "Error when trying stop device", 500

        return jsonify(True)

    @router.route("/device/stream")
    def stream():
        device_id = request.args.get('device')

        device = device_manager.get_device(device_id)
        mimetype = 'text/event-stream'

        if device is None:
            return 'Invalid device id', 500

        if device_id == 'camera':
            mimetype = 'multipart/x-mixed-replace; boundary=frame'
        elif device_id == 'openbci_cython' or device_id == 'arduino_uno':
            mimetype = 'text/event-stream'

        device_manager.start_stream(device_id)

        def generator():
            while True:
                try:
                    item_device_id, data = device_manager.stream_queue.get()
                    if item_device_id == 'camera':
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                    elif item_device_id == 'openbci_cython' or device_id == 'arduino_uno':
                        yield f"event:{'upd'}\ndata:{data}\n\n"
                except GeneratorExit:
                    print(f'Stop stream for {device_id}')
                    device_manager.stop_stream(device_id)
                    return

        return Response(generator(), mimetype=mimetype)

    return router
