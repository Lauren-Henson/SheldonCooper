#calculate gravitational force between particles
import numpy as np

const_G=4.3*10**(-3) # in the unit of (pc / solar mass^-1 * (km/s)^2)


class Particle:
    """
    A class to represent a particle in a simulation.

    Attributes:
    mass : float
        The mass of the particle.
    position : numpy.ndarray
        The position of the particle in 3D space.
    vel : numpy.ndarray
        The velocity of the particle in 3D space.
    acc : numpy.ndarray
        The acceleration of the particle in 3D space.
    time : float
        The time at which the properties of the particle are evaluated.
    seq : int
        The sequence number of the particle for identification.
    """

    def __init__(self, mass, position, vel, acc, seq):
        """
        Initializes a Particle object with its mass, position, velocity, 
        acceleration, and sequence number.

        Parameters:
        mass : float
            The mass of the particle.
        position : numpy.ndarray
            The initial position of the particle as a 3D vector.
        vel : numpy.ndarray
            The initial velocity of the particle as a 3D vector.
        acc : numpy.ndarray
            The initial acceleration of the particle as a 3D vector.
        seq : int
            The sequence number of the particle.
        """
        self.mass = mass
        self.position = position
        self.vel = vel
        self.acc = acc
        self.time = 0  # Initialize time to 0
        self.seq = seq

    def update_time(self, new_time):
        """
        Updates the time attribute of the particle.

        Parameters:
        new_time : float
            The new time value to be set for the particle.
        """
        self.time = new_time
    
    def cal_gforce(self, p_array):
        """
        Calculates the gravitational acceleration on the particle 
        due to other particles in the array.

        For each particle other than itself, the function calculates 
        the relative position and computes the gravitational force, 
        updating the acceleration of the particle accordingly.

        Parameters:
        p_array : list
            A list of Particle objects that represent other particles in the simulation.
        """
        self.acc = np.zeros(3)  # Reset acceleration to zero
        for i in range(len(p_array)):
            if i != self.seq:  # Skip self to avoid self-interaction
                del_pos = np.array(p_array[i].position - self.position)  # Calculate relative position
                rr = np.sqrt(np.sum(del_pos**2))  # Calculate the distance from the particle
                self.acc += p_array[i].mass * del_pos / rr**3  # Update acceleration based on gravitational force

        self.acc *= const_G  # Scale the acceleration by the gravitational constant



if __name__=="__main__":
    p_array=[]
    pp=np.array([0,0,0])
    vv=np.array([0,0,0])
    aa=np.array([0,0,0])
    p_array.append(Particle(1,pp,vv,aa,0))
    pp=np.array([1,0,0])
    p_array.append(Particle(1,pp,vv,aa,1))
    pp=np.array([0,1,0])
    p_array.append(Particle(1,pp,vv,aa,2))
    p_array=np.array(p_array)
    p_array[1].cal_gforce(p_array)
    print(p_array[1].acc)