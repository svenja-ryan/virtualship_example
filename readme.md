# VirtualShip Quick Start

This is a repository that distilles information provided from the virtualship developers/website to be used for teaching in 12.808. 

## 1. What is VirtualShip?

[VirtualShip](https://virtualship.parcels-code.org/) is a command-line simulator for planning and carrying out a virtual oceanographic research expedition. It uses ocean-model data to simulate measurements from instruments such as CTDs, ADCPs, surface drifters, Argo floats, and XBTs.

Useful documentation:

- [VirtualShip website](https://virtualship.parcels-code.org/)
- [Quickstart guide](https://virtualship.readthedocs.io/en/stable/user-guide/quickstart.html)
- [Working with `expedition.yaml`](https://virtualship.readthedocs.io/en/stable/user-guide/tutorials/working_with_expedition_yaml.html)
- [Pre-downloading input data](https://virtualship.readthedocs.io/en/stable/user-guide/documentation/pre_download_data.html)

## 2. Install the Python environment

VirtualShip is easiest to install with Conda or Micromamba:

```bash
conda create -n virtualship -c conda-forge virtualship
conda activate virtualship
```

Check that the command is available:

```bash
virtualship --version
virtualship --help
```


## 3. Initialize a cruise

Create a new expedition directory with an example configuration:

```bash
virtualship init MY_CRUISE
```

This creates a directory containing an `expedition.yaml` file.

If you have exported a route from the NIOZ Marine Facilities Planning tool, initialize from the route file instead:

```bash
virtualship init MY_CRUISE --from-mfp CoordinatesExport.xlsx
```

The route file should contain waypoint coordinates in decimal degrees.

## 4. Modify `expedition.yaml`

Open the file in a text editor:

```bash
cd MY_CRUISE
nano expedition.yaml
```

The main sections are:

```yaml
schedule:
  waypoints:
    - instrument:
        - CTD
        - DRIFTER
      location:
        latitude: 40.0
        longitude: -70.0
      time: 2026-06-01 12:00:00

instruments_config:
  drifter_config: ...

ship_config:
  ship_speed_knots: 10.0
```

Important cautions:

- YAML indentation matters. Use spaces, not tabs.
- Times must use `YYYY-MM-DD HH:MM:SS` format.
- Coordinates must be decimal degrees, with longitude between -180 and 180 and latitude between -90 and 90.
- Waypoint times must be physically realistic for the ship speed. The ship must have enough time to travel between waypoints.
- Instrument names are case-sensitive: `CTD`, `DRIFTER`, `ARGO_FLOAT`, and `XBT`.
- A drifter is deployed at the waypoint time and then continues drifting after the ship leaves. Make sure the input velocity data cover the complete drifter lifetime, not only the ship's cruise period.
- For drifters, input data must also cover the area into which the particle may drift. Otherwise the simulation may stop with a spatial or temporal out-of-bounds error.
- If using pre-downloaded daily data, include data beginning before the earliest drifter deployment and continuing through the entire drift. A missing first-day or preceding file can produce a Parcels `TimeExtrapolationError`.
- Do not add arbitrary parameters to `expedition.yaml`. Options such as Parcels' `allow_time_extrapolation=True` are internal Python settings and are not normally configured in the YAML file.

For larger expeditions, you can edit the file directly. Alternatively, use the graphical planning tool:

```bash
virtualship plan MY_CRUISE
```

## 5. Run the cruise

From the directory containing the expedition folder, run:

```bash
virtualship run MY_CRUISE
```

VirtualShip may prompt for Copernicus Marine credentials when it first downloads model data. Results are written to:

```text
MY_CRUISE/results/
```


For a first test, run a small expedition with one or two waypoints and without drifters. Once that completes successfully, add the drifter deployments and verify that the physical-data time and spatial coverage extend through the full drift period.
