# 快·开 (kuai kai)

## Abstract

We propose a system for continuous evaluation of autonomous driving capabilities
in high-speed racetracks. In the first implementation, the vehicles used on the
racetrack will be small (1/16 or 1/10 of full-size). User-submitted controllers
are evaluated remotely on real cars that can complete a racetrack circuit. Lap
times are saved to a leaderboard that ranks submissions according to best
(smallest) times. Potential users must pass simulation tests and, then,
hardware-in-the-loop simulations, before being granted time with the real cars
on the racetrack.

## Websites

Documentation releases are available at
https://kuaikai.readthedocs.io/

## Organization

Each directory that contains the source code of a major component will have a
README that introduces it.

* `acarbroker`: Web app for receiving user submissions and evaluating them in
  pure simulation and, then, hardware-in-the-loop simulation.

* `cars`: source code for support of specific car models.

* `doc`: sources for the user guide, developer guide, references, implementation
  details about hardware-in-the-loop simulation, racetrack layout, etc.  The
  documentation is written using [reStructuredText](
  http://docutils.sourceforge.net/rst.html) and built with [Sphinx](
  https://sphinx.readthedocs.io/).


## License

This is free software, released under the Apache License, Version 2.0.
You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
