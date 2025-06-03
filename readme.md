# Pico

Handles display of received images from a given url.
 

Includes a configurable event loop to handle calls, as well as easy to configure new displays/new image types.


Utilises Pimoroni firmware for their inclusion of Pimoroni screen drivers, although should be able to work on non-specific firmware with mild modifications

## Setup

### Pico

Grab the latest [Pimoroni firmware](https://github.com/pimoroni/pimoroni-pico-rp2350).

 Currently tested with 
[pico2_w-v0.0.11-pimoroni-micropython.uf2](https://github.com/pimoroni/pimoroni-pico-rp2350/releases/tag/v0.0.11).

### Config

Modify the `config.py` to the chosen display and preferred image format

### Secrets

```bash
cp secrets_example.py secrets.py
```

and fill them in 

## Development
 Create a virtual env and follow:
 
  https://github.com/pimoroni/pimoroni-pico-stubs
