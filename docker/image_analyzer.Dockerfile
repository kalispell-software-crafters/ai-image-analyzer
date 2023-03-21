ARG PYTHON_VERSION="3.9.13"
ARG PLATFORM_NAME="linux/amd64"

FROM --platform=${PLATFORM_NAME} python:${PYTHON_VERSION}

# --- SYSTEM ARCHITECTURE
ARG TARGETPLATFORM
ARG TARGETARCH
ARG TARGETVARIANT

RUN printf "I'm building for TARGETPLATFORM=${TARGETPLATFORM}" \
    && printf ", TARGETARCH=${TARGETARCH}" \
    && printf ", TARGETVARIANT=${TARGETVARIANT} \n" \
    && printf "With uname -s : " && uname -s \
    && printf "and  uname -m : " && uname -mm

# --- Environment variables
ENV REQUIREMENTS_FILE="requirements.txt"
ENV OUTDIR="/root"
ENV PROJECT_DIR="/opt/ml"
ENV PROGRAM_DIR="/opt/program"
ENV HOME_DIR="/root/ml"
ENV LOCAL_DEV_DIR="docker"
ENV ALIASES_FILE="/root/aliases.sh"
ENV DEBIAN_FRONTEND=noninteractive

# --- Dockerfile Metadata
LABEL Maintainer="Victor Calderon and Travis Craft"

# ------------------------- COPYING AND DIRECTORIES ---------------------------

RUN mkdir -p ${HOME_DIR}

COPY ./src ${PROJECT_DIR}/src
COPY ${LOCAL_DEV_DIR}/aliases.sh ${ALIASES_FILE}

COPY ${REQUIREMENTS_FILE} "${HOME_DIR}/${REQUIREMENTS_FILE}"

# ---------------------- EXPOSING PORTS FOR APP -------------------------------

EXPOSE 80
EXPOSE 8501

# --------------------- INSTALLING EXTRA PACKAGES -----------------------------
# --- Updating packages and installing packages at the system-level

RUN apt-get -y update && \
    apt-get upgrade -y && \
    apt-get clean && \
    # Instaling system-level packages
    apt-get install -y \
    git \
    ssh \
    tree \
    git-flow \
    tmux \
    direnv \
    bash-completion \
    zsh \
    htop \
    && \
    # Cleaning out
    rm -rf /var/lib/apt/lists/* && \
    # Cleaning installs
    apt-get clean && \
    # Installing ZSH and OhZSH
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    echo "source /etc/profile.d/bash_completion.sh" >> /root/.bashrc && \
    echo "source /etc/profile.d/bash_completion.sh" >> /root/.zshrc && \
    echo "source /root/aliases.sh" >> "${OUTDIR}/.zshrc" && \
    echo "source /root/aliases.sh" >> "${OUTDIR}/.bashrc" && \
    # Install direnv
    echo 'eval "$(direnv hook zsh)"' >> "${OUTDIR}/.zshrc" && \
    echo 'eval "$(direnv hook bash)"' >> "${OUTDIR}/.bash"

# -------------------------- DOCKER-SPECIFIC ----------------------------------

RUN apt-get update -y && \
    cd ${OUTDIR_DOCKER} && \
    curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# --------------------------- PYTHON-RELATED-LOCAL ----------------------------

RUN pip install --upgrade pip && \
    python -m pip install -r "${HOME_DIR}/${REQUIREMENTS_FILE}"

# Temporary fix for PyTube's error: https://github.com/pytube/pytube/issues/1498
ENV CIPHER_FILEPATH="/usr/local/lib/python3.9/site-packages/pytube/cipher.py"
RUN sed -i 's/findall(transform_plan_raw)/findall(js)/g' \
    ${CIPHER_FILEPATH} && \
    sed  -i 's/transform_plan_raw/#transform_plan_raw/g' \
    ${CIPHER_FILEPATH}

# ----------------------------- PYTHON-SPECIFIC -------------------------------

# Set some environment variables. PYTHONUNBUFFERED keeps Python from
# buffering our standard output stream, which means that logs can be
# delivered to the user quickly. PYTHONDONTWRITEBYTECODE keeps Python
# from writing the .pyc files which are unnecessary in this case. We also
# update PATH so that the train and serve programs are found when the
# container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="${PROGRAM_DIR}:${PATH}"
ENV PYTHONPATH="${PROGRAM_DIR}:${PYTHONPATH}"

WORKDIR ${PROJECT_DIR}

CMD ["uvicorn", "src.api.index:app", "--host", "0.0.0.0","--port", "80"]
