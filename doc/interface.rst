Interface
=========

Introduction
------------

The purpose of this section is to document the interface available to
submissions from users.

.. WARNING::
   Until the first version release, details of the interface can change without
   notice.

Requirements of submission
--------------------------

All shell scripts are run in ``bash``. If any script has nonzero exitcode, or if
a timeout is reached in any evaluation context, then the trial ends immediately
and is marked as failure.

1. ``build.sh``: run once at the start of the simulation, and not called
   again. The purpose of this script is to build executable files that are used
   in all evaluation texts. To reduce load on computer resources, the build
   process should only occur once.
2. ``start.sh``: start the controller in each of the evaluation contexts:
   simulation, hardware-in-the-loop sim, actual car on racetrack.
3. ``stop.sh``: stop the controller. The purpose of this script is to allow
   clean shutdown of the controller when some termination conditions are met,
   e.g., finally passing the finish line on the racetrack.
4. ``post.sh``: run at end of trial, after a successful call to ``stop.sh``,
   e.g., if user wants to upload logs to somewhere off-site

Any other files can be included, at the choice of the participant, but there is
a file size bound. Every context in which user-submitted code is running has a
time bound. Furthermore, there are bounds on available computational resources,
such as memory size. At this time, the bounds are not fixed.

Trials and jobs
---------------

The entire evaluation of a submission is referred to as a **trial**. Evaluation
is performed as a sequence of **jobs**, beginning with simulation. If any job
ends with failure, then the trial stops and is marked as failure. Otherwise,
measurements from the final job of executing the submitted controller on a
freely moving car are saved from completed trials.
