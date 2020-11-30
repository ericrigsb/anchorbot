FROM python:3
WORKDIR /usr/src/app
# Install the latest version of Firefox:
RUN export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests -y \
    # Firefox dependencies:
    libx11-xcb1 \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    bzip2 \
  && DL='https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64' \
  && curl -sL "$DL" | tar -xj -C /opt \
  && ln -s /opt/firefox/firefox /usr/local/bin/ \
  # Remove obsolete files:
  && apt-get autoremove --purge -y \
    bzip2 \
  && apt-get clean \
  && rm -rf \
    /tmp/* \
    /usr/share/doc/* \
    /var/cache/* \
    /var/lib/apt/lists/* \
    /var/tmp/*
# Install geckodriver
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` \
  && wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
  && tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin \
  && chmod +x /usr/local/bin/geckodriver \
  && rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY anchorbot.py .
CMD ["anchorbot.py"]
ENTRYPOINT ["python3"]