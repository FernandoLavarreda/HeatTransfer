"""
Fernando Jose Lavarreda Urizar
Gradient analysis for Unidemensional Transiet Heat Conduction App
Spheres, Walls and Cylinders
"""

import webbrowser
from gui import gui
from controller import controls
from conversion import conversion
from transient_analysis import ganalysis
from functools import partial

#print(ganalysis.temp_profile(typ_='c', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, dx=0.005, nlambdas=7, alfa=33.9e-6))

COMS = ["biot_", "st", "at", "length", "cond", "conv", "cp", "density", "alfa", "time_", "nlambdas", "dx", "coord"]



def main_(typ_:str, ui:gui.HeatImp, sym:bool=False, report:bool=False)->None:
    values = ui.get_parse_args()
    kwargs = {COMS[i]:values[i] for i in range(len(COMS))}
    if not report:
        coordinates = 0
        temperatures = 1
    else:
        coordinates = 3
        temperatures = 4
    if type(kwargs["time_"]) == list:
        kwargs["times"] = kwargs["time_"]
        del kwargs["time_"]
        ui.get_graphics().clear()
        est = ganalysis.temp_profiles(typ_=typ_, detailed=report, **kwargs)
        if sym:
            xs = [controls.symmetry(est[coordinates])+est[coordinates] for i in range(len(est[temperatures]))]
            symmetry_y = controls.msymmetry(est[temperatures], factor=1)
            ys = [symmetry_y[i]+est[temperatures][i] for i in range(len(est[temperatures]))]
            ui.get_graphics().set_lims(xlims=[kwargs["length"]*-1, kwargs["length"]], ylims=[min([kwargs["st"], kwargs["at"]]), max([kwargs["st"], kwargs["at"]])])
            ui.get_graphics().make_animation([xs, ys])
        else:
            xs = [est[coordinates] for i in range(len(est[temperatures]))]
            ui.get_graphics().set_lims(xlims=[0, kwargs["length"]], ylims=[min([kwargs["st"], kwargs["at"]]), max([kwargs["st"], kwargs["at"]])])
            ui.get_graphics().make_animation([xs, est[temperatures]])
    else:
        if sym:
            est = ganalysis.temp_profile(typ_=typ_, detailed=report, **kwargs)
            ui.get_graphics().clear()
            xs = controls.symmetry(est[coordinates])+est[coordinates]
            ys = controls.symmetry(est[temperatures], factor=1)+est[temperatures]
            ui.get_graphics().static_drawing([xs, ys])
        else:
            est = ganalysis.temp_profile(typ_=typ_, detailed=report, **kwargs)
            ui.get_graphics().clear()
            ui.get_graphics().static_drawing([est[coordinates], est[temperatures]])
    if report:
        if "time_" not in kwargs:
            content = controls.make_report({"Thermal Diffusivity":est[0], "Biot":est[2]}, est[1], est[coordinates], est[temperatures], time_labels=kwargs["times"])
        else:
            content = controls.make_report({"Thermal Diffusivity":est[0], "Biot":est[2]}, est[1], est[coordinates], est[temperatures], time_labels=kwargs["time_"])
        sv = ui.save_file(content, "Save Report", ".html")
        if sv:
            webbrowser.open(sv)
        


if __name__ == "__main__":
    #Set unit systems
    unit_systems = {
                    "metric":(conversion.METRIC_TABLE, conversion.convert_metric),
                    "imperial":(conversion.IMPERIAL_TABLE, conversion.convert_imperial),
                    "mixed":({key:{unit:None for unit in list(conversion.METRIC_TABLE[key].keys())+list(conversion.IMPERIAL_TABLE[key].keys())} for key in conversion.METRIC_TABLE.keys()}, conversion.convert_metric),
    }
    app = gui.HeatImp(actions={}, unit_systems=unit_systems)
    app.iconbitmap(__file__.replace("main.py", "icon/icon.ico"))
    main = partial(main_, ui=app)
    app.get_command().add_action("run", main)
    app.get_command().add_action("q", app.destroy)
    app.get_command().add_action("quit", app.destroy)
    app.mainloop()
    








