"""
Fernando Jose Lavarreda Urizar
Gradient analysis for Unidemensional Transiet Heat Conduction App
Spheres, Walls and Cylinders
"""

from gui import gui
from controller import controls
from transient_analysis import ganalysis
from functools import partial

#print(ganalysis.temp_profile(typ_='c', st=20, at=500, length=0.02, cond=110, conv=120, time_=420, dx=0.005, nlambdas=7, alfa=33.9e-6))

COMS = ["biot_", "st", "at", "length", "cond", "conv", "cp", "density", "alfa", "time_", "nlambdas", "dx", "coord"]



def main_(typ_:str, ui:gui.HeatImp, sym=False)->None:
    values = ui.get_parse_args()
    kwargs = {COMS[i]:values[i] for i in range(len(COMS))}
    if type(kwargs["time_"]) == list:
        kwargs["times"] = kwargs["time_"]
        del kwargs["time_"]
        ui.get_graphics().clear()
        est = ganalysis.temp_profiles(typ_=typ_, **kwargs)
        if sym:
            xs = [controls.symmetry(est[0])+est[0] for i in range(len(est[1]))]
            symmetry_y = controls.msymmetry(est[1], factor=1)
            ys = [symmetry_y[i]+est[1][i] for i in range(len(est[1]))]
            ui.get_graphics().set_lims(xlims=[kwargs["length"]*-1, kwargs["length"]], ylims=[min([kwargs["st"], kwargs["at"]]), max([kwargs["st"], kwargs["at"]])])
            ui.get_graphics().make_animation([xs, ys])
        else:
            xs = [est[0] for i in range(len(est[1]))]
            ui.get_graphics().set_lims(xlims=[0, kwargs["length"]], ylims=[min([kwargs["st"], kwargs["at"]]), max([kwargs["st"], kwargs["at"]])])
            ui.get_graphics().make_animation([xs, est[1]])
    else:
        if sym:
            est = ganalysis.temp_profile(typ_=typ_, **kwargs)
            ui.get_graphics().clear()
            xs = controls.symmetry(est[0])+est[0]
            ys = controls.symmetry(est[1], factor=1)+est[1]
            ui.get_graphics().static_drawing([xs, ys])
        else:
            est = ganalysis.temp_profile(typ_=typ_, **kwargs)
            ui.get_graphics().clear()
            ui.get_graphics().static_drawing(est)




if __name__ == "__main__":
    app = gui.HeatImp(actions={})
    app.iconbitmap(__file__.replace("main.py", "icon/icon.ico"))
    main = partial(main_, ui=app)
    app.get_command().add_action("run", main)
    app.get_command().add_action("q", app.destroy)
    app.get_command().add_action("quit", app.destroy)
    app.mainloop()
    








