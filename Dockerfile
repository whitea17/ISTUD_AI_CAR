FROM dustynv/jetson-inference:r32.5.0

WORKDIR /ISTUD_AI_CAR
RUN pip3 install Jetson.GPIO
COPY . .

CMD ["./app.sh"]