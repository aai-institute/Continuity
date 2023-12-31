import torch
import matplotlib.pyplot as plt
from continuity.data.datasets import Sine
from continuity.operators import ContinuousConvolution
from continuity.plotting import plot_observation

# Set random seed
torch.manual_seed(0)


def test_convolution():
    # Parameters
    num_sensors = 16
    num_evals = num_sensors

    # Observation
    dataset = Sine(num_sensors, size=1)
    observation = dataset.get_observation(0)

    # Kernel
    def dirac(x, y):
        dist = ((x - y) ** 2).sum(dim=-1)
        return torch.isclose(dist, torch.zeros(1)).to(torch.float32)

    # Operator
    operator = ContinuousConvolution(
        kernel=dirac,
        coordinate_dim=dataset.coordinate_dim,
        num_channels=dataset.num_channels,
    )

    # Create tensors
    x, u = observation.to_tensors()
    y = torch.linspace(-1, 1, num_evals).unsqueeze(-1)

    # Apply operator
    v = operator(x, u, y)

    # Extract batch
    v = v.squeeze(0)

    # Plotting
    fig, ax = plt.subplots(1, 1)
    plot_observation(observation, ax=ax)
    plt.plot(x, v, "o")
    fig.savefig(f"test_convolution.png")

    # For num_sensors == num_evals, we get v = u / num_sensors.
    if num_sensors == num_evals:
        v_expected = u / num_sensors
        assert (v == v_expected).all(), f"{v} != {v_expected}"


if __name__ == "__main__":
    test_convolution()
