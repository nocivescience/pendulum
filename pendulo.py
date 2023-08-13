from manim import *
class Pendulum(VGroup):
    configuration = {
        'mass_config':{
            'radius': 0.5,
            'color': BLUE,
        },
        'string_config':{
            'color': WHITE,
            'stroke_width': 3,
        },
        'origin': ORIGIN,
        'theta_max': PI/4,
        'theta_offset': 0,
        'theta_start': None,
        'length': 5,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mass = self.get_mass()
        self.string = self.get_string()
        self.string.save_state()
        self.string.initial_state = self.string.copy()
        if self.configuration['theta_start'] is None:
            self.configuration['theta_start'] = self.configuration['theta_max']
        self.mass.add_updater(lambda m: m.move_to(self.string.get_end()))
        self.rotate(self.configuration['theta_start'])
        self.add(self.string, self.mass)
    def get_mass(self):
        return Dot(**self.configuration['mass_config'])
    def get_string(self):
        return Line(
            self.configuration['origin']+3.4*UP,
            self.mass.get_center(),
            **self.configuration['string_config']
        ).set_z_index(-1)
    def rotate(self, angle):
        self.string.rotate(angle, about_point=self.string.get_start())
    def get_angle(self):
        return angle_between_vectors(self.string.get_unit_vector(), DOWN)*180/PI
    def restore_string(self):
        self.string.restore()
    def add_mass_update(self):
        self.mass.add_updater(lambda m: m.move_to(self.string.get_start()))
class PendulumScene(Scene):
    configu = {
        'line_config':{
            'color': WHITE,
            'stroke_width': 3,
        },
        'factor': 13,
    }
    def construct(self):
        pendulum = Pendulum()
        roof = self.get_roof(**self.configu['line_config'])
        self.play(Create(pendulum), Create(roof))
        self.play(Rotating(
            pendulum.string,
            radians=10*DEGREES,
            about_point=pendulum.string.get_start(),
            run_time=2,
        ))
        pendulum.add_updater(
            self.get_theta_func(pendulum)
        )
        self.add(pendulum)
        self.wait(12)
    def get_roof(self,size=.2,**line_config):
        line=Line(
            ORIGIN,
            UR*size,
            **line_config,
        )
        lines=VGroup(*[
            line.copy().shift(DOWN*size)
            for _ in range(30)
        ])
        lines.arrange(RIGHT,buff=0)
        down_line=Line(
            lines.get_corner(DL),
            lines.get_corner(DR),
            **line_config,
        )
        return VGroup(lines,down_line).move_to(3.5*UP)
    def get_theta_func(self,mob):
        func= lambda t: mob.configuration['theta_max']*np.cos(t*np.sqrt(9.8/mob.configuration['length']))
        def update_theta(mob,dt):
            mob.configuration['theta_offset']+=dt*3
            new_theta=func(mob.configuration['theta_offset'])
            mob.restore_string()
            mob.rotate(new_theta)
        return update_theta