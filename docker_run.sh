#/bin/bash -xe

VENV=.venv-docker
COMMAND=${1:-none}

IMAGE_TAG=${IMAGE_TAG:-pytorch/pytorch:2.3.1-cuda12.1-cudnn8-devel}
DATA_DIR=${DATA_DIR:-$HOME}

docker_run()
{
    cmd=$1
    docker run \
        --gpus all \
        --rm \
        --shm-size=8g \
        -p 7860:7860 \
        -it \
        -v `pwd`:/app \
        -v $DATA_DIR/repos/Unique3D/ckpt:/app/ckpt \
        -v $DATA_DIR/.cache/huggingface/hub:/root/.cache/huggingface/hub \
        -w /app \
        $IMAGE_TAG \
        $cmd
}


case $COMMAND in
    attach)
        docker_run bash
        ;;
    setup)
        docker_run "/app/setup.sh $VENV"
        ;;
    *)
        docker_run "/app/run.sh $VENV"
        ;;
esac

