# Home Surveillance System (HSS)

HSS is a Python-based home surveillance system that captures video from a webcam and detects motion using OpenCV. The system can send email alerts when motion is detected and record video of the motion.

## Installation

To install HSS, you need to have Python 3 and the following Python libraries installed:

- Flask
- OpenCV

You can install these libraries using pip:

## Usage

To use HSS, run the `webcam_capture.py` file:


This will start the Flask web server and open the web interface in your default web browser. The web interface displays the video stream from your webcam and highlights any motion detected in the video.

## Configuration

You can configure the following settings in the `config.py` file:

- `SMTP_SERVER`: The SMTP server used to send email alerts.
- `SMTP_PORT`: The SMTP server port.
- `SMTP_USERNAME`: Your email username.
- `SMTP_PASSWORD`: Your email password.
- `ALERT_RECIPIENTS`: A list of email addresses to receive motion detection alerts.
- `MOTION_THRESHOLD`: The minimum area of a contour to be considered as motion.
- `VIDEO_FILENAME`: The filename of the recorded video.

## Contributing

If you would like to contribute to HSS, please submit a pull request or open an issue on the GitHub repository.

## License

HSS is licensed under the MIT License. See the `LICENSE` file for more information.
