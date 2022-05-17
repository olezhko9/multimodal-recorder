from flask import Blueprint, request, jsonify, Response
from service import device_service


def get_device_api(device_manager):
    router = Blueprint('device_router', __name__)

    @router.route("/devices")
    def devices():
        res = device_service.get_devices()
        return jsonify(res)

    @router.route('/device/start', methods=['POST'])
    def start_device():
        try:
            device = request.json
            device_id = device['device_id']

            device_params = {}
            if device.get('settings'):
                for param in device['settings']:
                    device_params[param['name']] = param['value']

            device_manager.add_and_run_device(device_id, device_params)
            device_manager.read_data()
        except Exception:
            device_manager.stop_and_remove_devices()
            return "Error when trying connect to device", 500

        return jsonify(True)

    @router.route('/device/stop', methods=['POST'])
    def stop_device():
        try:
            device_id = request.json['device_id']
            device_manager.stop_and_remove_device(device_id)
        except:
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
        elif device_id == 'openbci_cython':
            mimetype = 'text/event-stream'

        device_manager.start_stream(device_id)

        def generator():
            while True:
                try:
                    item_device_id, data = device_manager.stream_queue.get()
                    if item_device_id == 'camera':
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')
                    elif item_device_id == 'openbci_cython':
                        yield f"event:{'upd'}\ndata:{data}\n\n"
                except GeneratorExit:
                    device_manager.stop_stream(device_id)
                    return

        return Response(generator(), mimetype=mimetype)

    return router
