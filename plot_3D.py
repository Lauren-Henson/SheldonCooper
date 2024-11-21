
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

from initial_conditions_3d import boltzmann_ini_positions



def visualization(position, mass, lim_bound=(-100, 100), window_size=300, interval=30, frame_rotation=0., savegif=False, fname=None):
    # Set up figure & 3D axis for animation
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # choose a different color for each particle
    num_particles = position.shape[0]
    # colors = plt.cm.jet(np.linspace(0, 1, num_particles))
    colors = plt.cm.jet(mass/np.max(mass))

    # set up lines and points for each particle
    lines = sum([ax.plot([], [], [], '-', c=colors[i]) for i in range(num_particles)], [])
    pts = sum([ax.plot([], [], [], 'o', c=colors[i]) for i in range(num_particles)], [])

    ## change the axes limits to boundary size
    ax.set_xlim(lim_bound)
    ax.set_ylim(lim_bound)
    ax.set_zlim(lim_bound)

    # set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(30, 0)

    # initialization function: plot the background of each frame
    def init():
        for line, pt in zip(lines, pts):
            line.set_data([], [])
            line.set_3d_properties([])

            pt.set_data([], [])
            pt.set_3d_properties([])
        return lines + pts

    # animation function.  This will be called sequentially with the frame number
    def animate(i):
        start = max(0, i - window_size + 1)  # Starting index for the window
        end = i + 1  # Ending index for the window

        # Update the lines to show only the most recent timesteps for each particle
        for line, idx in zip(lines, range(num_particles)):
            x, y, z = position[idx, start:end].T  # Extract coordinates for the current window
            line.set_data(x, y)  # Update line data for x and y
            line.set_3d_properties(z)  # Update line data for z

        # Update the points for all particles to reflect their current position
        for pt, xi in zip(pts, position):
            x, y, z = xi[i]  # Get the current coordinates for the particle
            pt.set_data([x], [y])  # Update point data for x and y
            pt.set_3d_properties([z])  # Update point data for z
        
        # ax.view_init(30, frame_rotation * i)  # Animate the viewpoint, by default it is not rotating
        
        fig.canvas.draw()

        return lines + pts

    # instantiate the animator.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=position.shape[1], interval=interval, blit=True)
    
    # save the animation automatically to /gif folder
    if savegif and fname is not None:
        if fname.endswith('.gif'):
            anim.save('./gif/'+fname, writer='pillow')
        else:
            raise ValueError('Only .gif format is supported for saving animation.')
    elif savegif and fname is None:
        raise ValueError('Please provide a filename to save the animation.')

    plt.show()




if __name__ == '__main__':
    # we generate the initial position 50 times to make 50 fake time steps
    step = 50
    n = 10
    position_matrix = np.empty((n, step, 3))

    for s in range(step):   # Iterate through each time step
        pos_temp = boltzmann_ini_positions(N=n, boundary_size=100, sigma_pos=50)
        position_matrix[:, s, :] = pos_temp

    visualization(position_matrix)