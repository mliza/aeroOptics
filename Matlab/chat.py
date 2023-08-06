import numpy as np
import matplotlib.pyplot as plt

# Constants
q = 1.602e-19   # charge of an electron
m = 9.109e-31   # mass of an electron
k = 1.381e-23   # Boltzmann constant
eps0 = 8.854e-12 # permittivity of free space

# Simulation parameters
Lx = 1.0e-6     # length of the simulation box in x-direction
Ly = 1.0e-6     # length of the simulation box in y-direction
Nx = 50         # number of grid points in x-direction
Ny = 50         # number of grid points in y-direction
dx = Lx/Nx      # grid spacing in x-direction
dy = Ly/Ny      # grid spacing in y-direction
dt = 1.0e-12    # time step
nt = 100        # number of time steps

# Particle parameters
np.random.seed(0) # set random seed for reproducibility
Np = 100         # number of particles
x = Lx*np.random.rand(Np) # initial x positions
y = Ly*np.random.rand(Np) # initial y positions
vx = np.zeros(Np) # initial x velocities
vy = np.zeros(Np) # initial y velocities
q = -q*np.ones(Np) # all particles have the same charge
m = m*np.ones(Np) # all particles have the same mass

# Initialize the electric field and charge density arrays
Ex = np.zeros((Nx+1,Ny))
Ey = np.zeros((Nx,Ny+1))
rho = np.zeros((Nx,Ny))

# Main loop
for n in range(nt):

    # Calculate the charge density
    rho *= 0.0
    for i in range(Np):
        ix = int(x[i]/dx)
        iy = int(y[i]/dy)
        rho[ix,iy] += q[i]/(dx*dy)

    # Calculate the electric field using Poisson's equation
    Ex[1:-1,:] = Ex[1:-1,:] - dt*(rho[2:,:] - rho[:-2,:])/(2*eps0*dx)
    Ey[:,1:-1] = Ey[:,1:-1] - dt*(rho[:,2:] - rho[:,:-2])/(2*eps0*dy)

    # Move the particles using the electric field
    for i in range(Np):
        ix = int(x[i]/dx)
        iy = int(y[i]/dy)
        vx[i] += q[i]*Ex[ix,iy]/m[i]*dt
        vy[i] += q[i]*Ey[ix,iy]/m[i]*dt
        x[i] += vx[i]*dt
        y[i] += vy[i]*dt

    # Periodic boundary conditions
    x = np.mod(x,Lx)
    y = np.mod(y,Ly)

    # Plot the results every 10 time steps
    if n % 10 == 0:
        plt.clf()
        plt.scatter(x,y,color='r')
        plt.xlim([0,Lx])
        plt.ylim([0,Ly])
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.title('Particle-in-Cell Simulation')
        plt.pause(0.001)
