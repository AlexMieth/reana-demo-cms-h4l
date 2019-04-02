===========================================
 REANA example - CMS Higgs-to-four-leptons
===========================================

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/reanahub/reana?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/reanahub/reana-demo-cms-h4l/blob/master/LICENSE

About
=====

This `REANA <http://www.reana.io/>`_ reproducible analysis example studies the
Higgs-to-four-lepton decay channel that led to the Higgs boson experimental
discovery in 2012. The example uses CMS open data released in 2011 and
2012.

Analysis structure
==================

Making a research data analysis reproducible basically means to provide
"runnable recipes" addressing (1) where is the input data, (2) what software was
used to analyse the data, (3) which computing environments were used to run the
software and (4) which computational workflow steps were taken to run the
analysis. This will permit to instantiate the analysis on the computational
cloud and run the analysis to obtain (5) output results.


1. Input data
-------------

The analysis takes the following inputs:

- the list of CMS validated runs included in the ``inputs`` directory:

  - ``Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt``

- a set of data files in the `ROOT <https://root.cern.ch/>`_ format, processed
  from CMS public datasets, included in the ``inputs`` directory:

  - ``DoubleE11.root``
  - ``DoubleE12.root``
  - ``DoubleMu11.root``
  - ``DoubleMu12.root``
  - ``DY1011.root``
  - ``DY1012.root``
  - ``DY101Jets12.root``
  - ``DY50Mag12.root``
  - ``DY50TuneZ11.root``
  - ``DY50TuneZ12.root``
  - ``DYTo2mu12.root``
  - ``HZZ11.root``
  - ``HZZ12.root``
  - ``TTBar11.root``
  - ``TTBar12.root``
  - ``TTJets11.root``
  - ``TTJets12.root``
  - ``ZZ2mu2e11.root``
  - ``ZZ2mu2e12.root``
  - ``ZZ4e11.root``
  - ``ZZ4e12.root``
  - ``ZZ4mu11.root``
  - ``ZZ4mu12.root``

- CMS collision data from 2011 and 2012 accessed "live" during analysis via
  `CERN Open Data <http://opendata.cern.ch/>`_ portal:

  - `/DoubleMuParked/Run2012C-22Jan2013-v1/AOD <http://opendata.cern.ch/record/6030>`_

- CMS simulated data from 2011 and 2012 accessed "live" during analysis via
  `CERN Open Data <http://opendata.cern.ch/>`_ portal:

  - `/SMHiggsToZZTo4L_M-125_8TeV-powheg15-JHUgenV3-pythia6/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM <http://opendata.cern.ch/record/9356>`_

2. Analysis code
----------------

The analysis will consist of two stages. In the first stage, we shall process
the original collision data (using ``demoanalyzer_cfg_level3data.py``) and
simulated data (using ``demoanalyzer_cfg_level3MC.py``) for one Higgs signal
candidate with with reduced statistics. In the second stage, we shall plot the
results (using ``M4Lnormdatall_lvl3.cc``). The ``HiggsDemoAnalyzer`` directory
contains the analysis code plugin for the `CMSSW <http://cms-sw.github.io/>`_
analysis framework.

3. Compute environment
----------------------

In order to be able to rerun the analysis even several years in the future, we
need to "encapsulate the current compute environment", for example to freeze the
software package versions our analysis is using. We shall achieve this by
preparing a `Docker <https://www.docker.com/>`_ container image for our analysis
steps.

This analysis example runs within the `CMSSW <http://cms-sw.github.io/>`_
analysis framework that was packaged for Docker in `clelange/cmssw
<https://hub.docker.com/r/clelange/cmssw/>`_.

4. Analysis workflow
--------------------

The analysis workflow is simple and consists of two above-mentioned stages:

.. code-block:: console

                              START
                             /     \
                            /       \
                           /         \
   +-------------------------+     +------------------------+
   | process collision data  |     | process simulated data |
   +-------------------------+     +------------------------+
                   \                       /
                    \ Higgs4L1file.root   / DoubleMuParked2012C_10000_Higgs.root
                     \                   /
                  +-------------------------+
                  |    produce final plot   |
                  +-------------------------+
                             |
                             | mass4l_combine_userlvl3.pdf
                             V
                            STOP

We shall use the `CWL <http://www.commonwl.org/v1.0/>`_ workflow specification
to express the computational workflow:

- `workflow definition <workflow/workflow.cwl>`_

and its individual steps:

- `process collision data <workflow/step1data.cwl>`_
- `process simulated data <workflow/step1mc.cwl>`_
- `produce final plot <workflow/step2.cwl>`_

5. Output results
-----------------

The example produces a plot showing the Higgs signal:

.. figure:: https://raw.githubusercontent.com/reanahub/reana-demo-cms-h4l/master/docs/mass4l_combine_userlvl3.png
   :alt: mass4l_combine_userlvl3.png
   :align: center

Local testing
=============

*Optional*

If you would like to test the analysis locally (i.e. outside of the REANA
platform), you can proceed as follows.

Using pure Docker:

.. code-block:: console

    $ docker run -i -t --rm \
           -v `pwd`/inputs:/inputs \
           -v `pwd`/code:/code \
           -v `pwd`/outputs:/outputs \
           clelange/cmssw:5_3_32 \
       /bin/bash -c 'cp -r /code/HiggsExample20112012 .; \
                     scram b; \
                     cd /code/HiggsExample20112012/Level3; \
                     cmsRun ./demoanalyzer_cfg_level3data.py'

    $ docker run -i -t --rm \
           -v `pwd`/inputs:/inputs \
           -v `pwd`/code:/code \
           -v `pwd`/outputs:/outputs \
           clelange/cmssw:5_3_32 \
       /bin/bash -c 'cp -r /code/HiggsExample20112012 .; \
                     scram b; \
                     cd /code/HiggsExample20112012/Level3; \
                     cmsRun demoanalyzer_cfg_level3MC.py'

    $ docker run -i -t --rm \
           -v `pwd`/inputs:/inputs \
           -v `pwd`/code:/code \
           -v `pwd`/outputs:/outputs \
           clelange/cmssw:5_3_32 \
       /bin/bash -c 'cd /code/HiggsExample20112012/Level3; \
                     root -b -l -q ./M4Lnormdatall_lvl3.cc'

Using CWL:

.. code-block:: console

    $ cwltool --outdir=./outputs ./workflow/workflow.cwl ./workflow/input.yaml

Running the example on CERN batch system using HTCondor
=======================================================

First log on to the CERN lxplus computing cluster using your CERN username and password:

.. code-block:: console

    $ ssh -Y username@lxplus.cern.ch

Set up a CMSSW working folder using the following command:

.. code-block:: console

    [username@lxplus### ~]$ cmsrel CMSSW_5_3_32

Clone the batch_work branch of this repository into the newly created src directory:

.. code-block:: console

    [username@lxplus### ~]$ cd CMSSW_5_3_32/src
    [username@lxplus### src]$ git clone -b batch_work https://github.com/AlexMieth/reana-demo-cms-h4l.git
    
Level 3
-------
Run stage 1 of the analysis by submitting the following jobs to the batch system. These jobs process the collision data and simulated Monte Carlo data.

.. code-block:: console

    [username@lxplus### src]$ cd reana-demo-cms-h4l/batch_files
    [username@lxplus### batch_files]$ condor_submit lvl3_data.sub
    [username@lxplus### batch_files]$ condor_submit lvl3_mc.sub
    
When these two jobs have been completed, you should now see two new files within the outputs directory: DoubleMuParked2012C_10000_Higgs.root and Higgs4L1file.root. Next, run stage 2 of the analysis by submitting the final job.

.. code-block:: console

    [username@lxplus### batch_files]$ condor_submit lvl3_combine.sub
    
This job combines the two previously generated output files and produces the final plot: mass4l_combine_userlvl3.pdf.

Level 4
-------
The first step of running Level 4 is generating the configuration files needed for stage 1 of the analysis. Go to the Level 4 directory and run level4_script.py. Use the '-n' flag to specify the number of root files you would like to analyze within each configuration file. Each of these configuration files will be run in parallel on the batch system so choosing a smaller number of files per job will decrease the total time needed for analysis but will increase the number of jobs needed to run on batch.

.. code-block:: console

    [username@lxplus### src]$ cd reana-demo-cms-h4l/code/HiggsExample20112012/Level4
    [username@lxplus### Level4]$ python3 ./level4_script -n 5
    
The newly generated configuration files should now be in the cfg_files directory. Now that we have generated all of the configuration files that we would like to run, we simply need to adjust the batch submission file to account for the correct number of jobs. Simply change the number at the end of the file after the word "queue" to match the number of configuration files that you generated.

At this point, simply move to the batch_files directory and submit the jobs to HTCondor.

.. code-block:: console

    [username@lxplus### Level4]$ cd ../../../batch_files
    [username@lxplus### batch_files]$ condor_submit lvl4_stage1.sub

FIXME

Running the example on REANA cloud
==================================

**FIXME**

Contributors
============

This example is based on the `original open data analysis
<http://opendata.cern.ch/record/5500>`_ by Jomhari, Nur Zulaiha; Geiser, Achim;
Bin Anuar, Afiq Aizuddin, "Higgs-to-four-lepton analysis example using 2011-2012
data", CERN Open Data Portal, 2017. DOI: `10.7483/OPENDATA.CMS.JKB8.RR42
<https://doi.org/10.7483/OPENDATA.CMS.JKB8.RR42>`_

The list of contributors to this REANA example in alphabetical order:


- `Clemens Lange <https://orcid.org/0000-0002-3632-3157>`_ <clemens.lange@cern.ch>
- Diyaselis Delgado Lopez <diyaselis.delgado.lopez@cern.ch>
- `Tibor Simko <https://orcid.org/0000-0001-7202-5803>`_ <tibor.simko@cern.ch>
