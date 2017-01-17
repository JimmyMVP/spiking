
import nest
import pylab

simtime = 100.0           # ms
stim_current = 700.0           # pA
resolutions = [0.1, 0.5, 1.0]  # ms

data = {}

for h in resolutions:
    data[h] = {}
    for model in ["iaf_psc_exp", "iaf_psc_exp_ps"]:
        nest.ResetKernel()
        nest.SetKernelStatus({'resolution': h})

        neuron = nest.Create(model)
        voltmeter = nest.Create("voltmeter", params={"interval": h})
        dc = nest.Create("dc_generator", params={"amplitude": stim_current})
        sd = nest.Create("spike_detector", params={"precise_times": True})

        nest.Connect(voltmeter, neuron)
        nest.Connect(dc, neuron)
        nest.Connect(neuron, sd)

        nest.Simulate(simtime)

        vm_status = nest.GetStatus(voltmeter, 'events')[0]
        sd_status = nest.GetStatus(sd, 'events')[0]
        data[h][model] = {"vm_times": vm_status['times'],
                          "vm_values": vm_status['V_m'],
                          "spikes": sd_status['times'],
                          "V_th": nest.GetStatus(neuron, 'V_th')[0]}

colors = ["#3465a4", "#cc0000"]

for v, h in enumerate(sorted(data)):
    plot = pylab.subplot(len(data), 1, v + 1)
    plot.set_title("Resolution: {0} ms".format(h))

    for i, model in enumerate(data[h]):
        times = data[h][model]["vm_times"]
        potentials = data[h][model]["vm_values"]
        spikes = data[h][model]["spikes"]
        spikes_y = [data[h][model]["V_th"]] * len(spikes)

        plot.plot(times, potentials, "-", c=colors[i], ms=5, lw=2, label=model)
        plot.plot(spikes, spikes_y, ".", c=colors[i], ms=5, lw=2)

    if v == 2:
        plot.legend(loc=4)
    else:
        plot.set_xticklabels('')