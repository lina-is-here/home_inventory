$(function () {
    var detectedCodes = [];
    var App = {
        init: function () {
            var self = this;

            Quagga.init(this.state, function (err) {
                if (err) {
                    return self.handleError(err);
                }
                //Quagga.registerResultCollector(resultCollector);
                App.attachListeners();
                App.checkCapabilities();
                Quagga.start();
            });
        },
        handleError: function (err) {
            console.log(err);
        },
        checkCapabilities: function () {
            var track = Quagga.CameraAccess.getActiveTrack();
            var capabilities = {};
            if (typeof track.getCapabilities === 'function') {
                capabilities = track.getCapabilities();
            }
            this.applySettingsVisibility('torch', capabilities.torch);
        },
        updateOptionsForMediaRange: function (node, range) {
            console.log('updateOptionsForMediaRange', node, range);
            var NUM_STEPS = 6;
            var stepSize = (range.max - range.min) / NUM_STEPS;
            var option;
            var value;
            while (node.firstChild) {
                node.removeChild(node.firstChild);
            }
            for (var i = 0; i <= NUM_STEPS; i++) {
                value = range.min + (stepSize * i);
                option = document.createElement('option');
                option.value = value;
                option.innerHTML = value;
                node.appendChild(option);
            }
        },
        applySettingsVisibility: function (setting, capability) {
            // depending on type of capability
            if (typeof capability === 'boolean') {
                var node = document.querySelector('input[name="settings_' + setting + '"]');
                if (node) {
                    node.parentNode.style.display = capability ? 'block' : 'none';
                }
                return;
            }
            if (window.MediaSettingsRange && capability instanceof window.MediaSettingsRange) {
                var node = document.querySelector('select[name="settings_' + setting + '"]');
                if (node) {
                    this.updateOptionsForMediaRange(node, capability);
                    node.parentNode.style.display = 'block';
                }
            }
        },
        initCameraSelection: function () {
            var streamLabel = Quagga.CameraAccess.getActiveStreamLabel();

            return Quagga.CameraAccess.enumerateVideoDevices()
                .then(function (devices) {
                    function pruneText(text) {
                        return text.length > 30 ? text.substr(0, 30) : text;
                    }

                    var $deviceSelection = document.getElementById("deviceSelection");
                    while ($deviceSelection.firstChild) {
                        $deviceSelection.removeChild($deviceSelection.firstChild);
                    }
                    devices.forEach(function (device) {
                        var $option = document.createElement("option");
                        $option.value = device.deviceId || device.id;
                        $option.appendChild(document.createTextNode(pruneText(device.label || device.deviceId || device.id)));
                        $option.selected = streamLabel === device.label;
                        $deviceSelection.appendChild($option);
                    });
                });
        },
        attachListeners: function () {
            var self = this;
            self.initCameraSelection();
            $(".controls").on("click", "button.stop", function (e) {
                e.preventDefault();
                Quagga.stop();
                jQuery("#barcode-scanner-container").hide();
                jQuery("#scan-barcode").show();
            });

            $(".controls .reader-config-group").on("change", "input, select", function (e) {
                e.preventDefault();
                var $target = $(e.target),
                    value = $target.attr("type") === "checkbox" ? $target.prop("checked") : $target.val(),
                    name = $target.attr("name"),
                    state = self._convertNameToState(name);

                console.log("Value of " + state + " changed to " + value);
                self.setState(state, value);
            });
        },
        _accessByPath: function (obj, path, val) {
            var parts = path.split('.'),
                depth = parts.length,
                setter = (typeof val !== "undefined") ? true : false;

            return parts.reduce(function (o, key, i) {
                if (setter && (i + 1) === depth) {
                    if (typeof o[key] === "object" && typeof val === "object") {
                        Object.assign(o[key], val);
                    } else {
                        o[key] = val;
                    }
                }
                return key in o ? o[key] : {};
            }, obj);
        },
        _convertNameToState: function (name) {
            return name.replace("_", ".").split("-").reduce(function (result, value) {
                return result + value.charAt(0).toUpperCase() + value.substring(1);
            });
        },
        detachListeners: function () {
            $(".controls").off("click", "button.stop");
            $(".controls .reader-config-group").off("change", "input, select");
        },
        applySetting: function (setting, value) {
            var track = Quagga.CameraAccess.getActiveTrack();
            if (track && typeof track.getCapabilities === 'function') {
                switch (setting) {
                    case 'torch':
                        return track.applyConstraints({advanced: [{torch: !!value}]});
                }
            }
        },
        setState: function (path, value) {
            var self = this;

            if (typeof self._accessByPath(self.inputMapper, path) === "function") {
                value = self._accessByPath(self.inputMapper, path)(value);
            }

            if (path.startsWith('settings.')) {
                var setting = path.substring(9);
                return self.applySetting(setting, value);
            }
            self._accessByPath(self.state, path, value);

            console.log(JSON.stringify(self.state));
            App.detachListeners();
            Quagga.stop();
            App.init();
        },
        inputMapper: {
            inputStream: {
                constraints: function (value) {
                    if (/^(\d+)x(\d+)$/.test(value)) {
                        var values = value.split('x');
                        return {
                            width: {min: parseInt(values[0])},
                            height: {min: parseInt(values[1])}
                        };
                    }
                    return {
                        deviceId: value
                    };
                }
            },
            numOfWorkers: function (value) {
                return parseInt(value);
            },
            decoder: {
                readers: function (value) {
                    if (value === 'ean_extended') {
                        return [{
                            format: "ean_reader",
                            config: {
                                supplements: [
                                    'ean_5_reader', 'ean_2_reader'
                                ]
                            }
                        }];
                    }
                    return [{
                        format: value + "_reader",
                        config: {}
                    }];
                }
            }
        },
        state: {
            inputStream: {
                type: "LiveStream",
                constraints: {
                    width: {min: 640},
                    height: {min: 480},
                    facingMode: "environment",
                    aspectRatio: {min: 1, max: 2}
                }
            },
            locator: {
                patchSize: "medium",
                halfSample: true
            },
            numOfWorkers: 2,
            frequency: 10,
            decoder: {
                readers: [{
                    format: "ean_reader",
                    config: {}
                }]
            },
            locate: false,
            area: {
                top: "20%",
                right: "20%",
                left: "20%",
                bottom: "20%"
            }
        },
        lastResult: null
    };

    $(".container").on("click", "button.scan", function ($) {
        jQuery("#scan-barcode").hide();
        jQuery("#barcode-scanner-container").show();
        App.init();
    });

    Quagga.onProcessed(function (result) {
        var drawingCtx = Quagga.canvas.ctx.overlay,
            drawingCanvas = Quagga.canvas.dom.overlay;

        if (result) {
            if (result.boxes) {
                drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
                result.boxes.filter(function (box) {
                    return box !== result.box;
                }).forEach(function (box) {
                    Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx, {color: "green", lineWidth: 2});
                });
            }

            if (result.box) {
                Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx, {color: "#00F", lineWidth: 2});
            }

            if (result.codeResult && result.codeResult.code) {
                Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx, {color: 'red', lineWidth: 3});
            }
        }
    });

    Quagga.onDetected(function (result) {
            var code = result.codeResult.code;
            detectedCodes.push(code)
            // if the last 3 scans are the same, it's more likely the correct barcode
            var codesLength = detectedCodes.length
            if (codesLength > 2 && (detectedCodes[codesLength - 1] === detectedCodes[codesLength - 2])
                &&
                (detectedCodes[codesLength - 1] === detectedCodes[codesLength - 3])
            ) {
                console.log(`Detected ${code} 3 times, proceeding...`)
                $('#id_barcode').val(code).trigger('input')
                Quagga.stop();
                jQuery("#barcode-scanner-container").hide();
                jQuery("#scan-barcode").show();
            }
        }
    );

})
;
