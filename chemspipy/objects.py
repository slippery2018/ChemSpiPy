# -*- coding: utf-8 -*-
"""
chemspipy.objects
~~~~~~~~~~~~~~~~~

Objects returned by ChemSpiPy API methods.

"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from .utils import memoized_property


class Compound(object):
    """ A class for retrieving and caching details about a specific ChemSpider record.

    The purpose of this class is to provide access to various parts of the ChemSpider API that return information about
    a compound given its ChemSpider ID. Information is loaded lazily when requested, and cached for future access.
    """

    def __init__(self, cs, csid):
        """

        :param ChemSpider cs: ``ChemSpider`` session.
        :param int|string csid: ChemSpider ID.
        """
        self._cs = cs
        self._csid = int(csid)
        # TODO: Allow optional initialize  with a record-type response from the API (kwarg or class method from_dict?).

    def __eq__(self, other):
        return isinstance(other, Compound) and self.csid == other.csid

    def __repr__(self):
        return 'Compound(%r)' % self.csid

    def _repr_png_(self):
        """For IPython notebook, display 2D image."""
        return self.image

    @property
    def csid(self):
        """ChemSpider ID."""
        return self._csid

    # TODO: csid setter that clears cached properties?

    @property
    def image_url(self):
        """Return the URL of a PNG image of the 2D chemical structure."""
        return 'http://www.chemspider.com/ImagesHandler.ashx?id=%s' % self.csid

    @memoized_property
    def _compound_info(self):
        """Request compound info and cache the result."""
        return self._cs.get_compound_info(self.csid)

    @memoized_property
    def _extended_compound_info(self):
        """Request extended compound info and cache the result."""
        return self._cs.get_extended_compound_info(self.csid)

    @property
    def molecular_formula(self):
        """Return the molecular formula for this Compound.

        :rtype: string
        """
        return self._extended_compound_info['molecular_formula']

    @property
    def smiles(self):
        """Return the SMILES for this Compound.

        :rtype: string
        """
        return self._compound_info['smiles']

    @property
    def stdinchi(self):
        """Return the Standard InChI for this Compound.

        :rtype: string
        """
        return self._compound_info['inchi']

    @property
    def stdinchikey(self):
        """Return the Standard InChIKey for this Compound.

        :rtype: string
        """
        return self._compound_info['inchikey']

    @property
    def inchi(self):
        """Return the InChI for this Compound.

        :rtype: string
        """
        return self._extended_compound_info['inchi']

    @property
    def inchikey(self):
        """Return the InChIKey for this Compound.

        :rtype: string
        """
        return self._extended_compound_info['inchikey']

    @property
    def average_mass(self):
        """Return the average mass of this Compound.

        :rtype: float
        """
        return self._extended_compound_info['average_mass']

    @property
    def molecular_weight(self):
        """Return the molecular weight of this Compound.

        :rtype: float
        """
        return self._extended_compound_info['molecular_weight']

    @property
    def monoisotopic_mass(self):
        """Return the monoisotopic mass of this Compound.

        :rtype: float
        """
        return self._extended_compound_info['monoisotopic_mass']

    @property
    def nominal_mass(self):
        """Return the nominal mass of this Compound.

        :rtype: float
        """
        return self._extended_compound_info['nominal_mass']

    @property
    def alogp(self):
        """Return the calculated AlogP for this Compound.

        :rtype: float
        """
        return self._extended_compound_info['alogp']

    @property
    def xlogp(self):
        """Return the calculated XlogP for this Compound.

        :rtype: float
        """
        return self._extended_compound_info['xlogp']

    @property
    def common_name(self):
        """Return the common name for this Compound.

        :rtype: string
        """
        return self._extended_compound_info['common_name']

    @memoized_property
    def mol_2d(self):
        """Return the MOL file for this Compound with 2D coordinates.

        :rtype: string
        """
        return self._cs.get_record_mol(self.csid, calc3d=False)

    @memoized_property
    def mol_3d(self):
        """Return the MOL file for this Compound with 3D coordinates.

        :rtype: string
        """
        return self._cs.get_record_mol(self.csid, calc3d=True)

    @memoized_property
    def image(self):
        """Return a 2D depiction of this Compound.

        :rtype: bytes
        """
        return self._cs.get_compound_thumbnail(self.csid)
