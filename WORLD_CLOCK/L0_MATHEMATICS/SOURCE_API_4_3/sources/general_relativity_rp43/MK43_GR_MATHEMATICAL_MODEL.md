# MK43 Ultra — General Relativity Mathematical Closure Model

Status: **MINIMAL COMPLETE CLOSURE GRAPH COMPLETE**

- Mathematical families: 19
- Canonical candidate objects: 340
- Typed dependency/realization edges: 705
- Core equation records: 52
- Missing edge endpoints: 0
- Weakly connected components: 1
- Root component size: 340/340

## Principal spine

```text
@graviton
↓ PROJECTS THROUGH
@time_shell_projection
↓ REALIZES
@metric_perturbation
↓ DEFINES
@readable_space_time
↓ CLOSES AS
@spacetime
↓ SUPPORTS
@levi_civita_connection
↓ GENERATES
@riemann_tensor
↓ CONTRACTS
@ricci_tensor
↓ COMPOSES
@einstein_tensor
↓ COUPLES TO
@stress_energy_tensor
↓ SATISFIES
@einstein_field_equation
↓ ADMITS
@black_hole
↓ BOUNDED BY
@event_horizon
↓ SUPPORTS
@quantum_field_in_curved_spacetime
↓ PRODUCES
@hawking_radiation
↓ CREATES
@black_hole_information_problem
↓ CONNECTS TO
@cosmology
```

## F0_MK43_ATTACHMENT

- `@graviton` — MK43 readable gravitational excitation  
  Dependencies: 0; dependents: 2.
- `@time_shell_projection` — MK43 native-to-readable projection  
  Dependencies: 1; dependents: 2.
- `@metric_perturbation` — Weak readable metric deformation  
  Dependencies: 3; dependents: 2.
- `@readable_space_time` — Readable spacetime realization  
  Dependencies: 1; dependents: 1.
- `@black_hole` — Black-hole recovery root  
  Dependencies: 3; dependents: 0.

## F1_DIFFERENTIAL_FOUNDATION

- `@smooth_manifold` — Smooth Hausdorff second-countable manifold  
  Dependencies: 0; dependents: 2.
- `@chart` — Smooth coordinate chart  
  Dependencies: 1; dependents: 1.
- `@atlas` — Compatible smooth atlas  
  Dependencies: 1; dependents: 0.
- `@smooth_map` — Smooth map between manifolds  
  Dependencies: 0; dependents: 0.
- `@diffeomorphism` — Invertible smooth map with smooth inverse  
  Dependencies: 0; dependents: 0.
- `@tangent_vector` — Derivation at a point  
  Dependencies: 0; dependents: 1.
- `@tangent_space` — Vector space of tangent vectors  
  Dependencies: 1; dependents: 1.
- `@tangent_bundle` — Bundle of tangent spaces  
  Dependencies: 1; dependents: 1.
- `@cotangent_space` — Dual tangent space  
  Dependencies: 0; dependents: 1.
- `@cotangent_bundle` — Bundle of cotangent spaces  
  Dependencies: 1; dependents: 1.
- `@vector_field` — Smooth tangent-bundle section  
  Dependencies: 1; dependents: 0.
- `@covector_field` — Smooth cotangent-bundle section  
  Dependencies: 1; dependents: 0.
- `@tensor_field` — Smooth tensor-bundle section  
  Dependencies: 0; dependents: 2.
- `@differential_form` — Alternating covariant tensor field  
  Dependencies: 1; dependents: 1.
- `@exterior_derivative` — Nilpotent derivative on forms  
  Dependencies: 1; dependents: 0.
- `@wedge_product` — Graded antisymmetric product  
  Dependencies: 0; dependents: 0.
- `@lie_bracket` — Commutator of vector fields  
  Dependencies: 0; dependents: 0.
- `@lie_derivative` — Derivative along a flow  
  Dependencies: 0; dependents: 0.
- `@pullback` — Contravariant transport of covariant objects  
  Dependencies: 0; dependents: 0.
- `@pushforward` — Covariant transport of tangent objects  
  Dependencies: 0; dependents: 0.
- `@orientation` — Choice of consistent volume orientation  
  Dependencies: 0; dependents: 1.
- `@volume_form` — Nowhere-vanishing top-degree form  
  Dependencies: 1; dependents: 0.
- `@partition_of_unity` — Smooth local-to-global gluing device  
  Dependencies: 0; dependents: 0.

## F2_LORENTZIAN_SPACETIME

- `@spacetime` — Connected four-dimensional time-oriented Lorentzian manifold  
  Dependencies: 1; dependents: 2.
- `@lorentzian_manifold` — Smooth manifold with Lorentzian metric  
  Dependencies: 2; dependents: 2.
- `@metric_tensor` — Nondegenerate symmetric (0,2) tensor  
  Dependencies: 2; dependents: 3.
- `@inverse_metric` — Inverse bilinear form  
  Dependencies: 1; dependents: 1.
- `@metric_signature` — Lorentzian inertia convention  
  Dependencies: 0; dependents: 0.
- `@line_element` — Metric interval representation  
  Dependencies: 1; dependents: 1.
- `@causal_character` — Timelike, null, or spacelike classification  
  Dependencies: 1; dependents: 1.
- `@light_cone` — Null cone in each tangent space  
  Dependencies: 1; dependents: 0.
- `@time_orientation` — Continuous future-cone choice  
  Dependencies: 1; dependents: 1.
- `@timelike_curve` — Curve with timelike tangent  
  Dependencies: 0; dependents: 0.
- `@null_curve` — Curve with null tangent  
  Dependencies: 0; dependents: 0.
- `@spacelike_curve` — Curve with spacelike tangent  
  Dependencies: 0; dependents: 0.
- `@proper_time` — Invariant timelike curve length  
  Dependencies: 0; dependents: 0.
- `@proper_distance` — Induced spatial length where defined  
  Dependencies: 0; dependents: 0.
- `@causal_future` — Set reachable by future causal curves  
  Dependencies: 1; dependents: 1.
- `@chronological_future` — Set reachable by future timelike curves  
  Dependencies: 0; dependents: 0.
- `@causal_past` — Set reaching a point by future causal curves  
  Dependencies: 0; dependents: 0.
- `@chronological_past` — Set reaching a point by future timelike curves  
  Dependencies: 0; dependents: 0.
- `@causal_structure` — Partial-order-like structure from causal curves  
  Dependencies: 1; dependents: 1.
- `@domain_of_dependence` — Region fixed by data on an achronal set  
  Dependencies: 1; dependents: 1.
- `@cauchy_surface` — Achronal set met exactly once by inextendible causal curves  
  Dependencies: 1; dependents: 1.
- `@global_hyperbolicity` — Strong causality plus compact causal diamonds  
  Dependencies: 1; dependents: 3.
- `@globally_hyperbolic_splitting` — Spacetime splitting into time and Cauchy slices  
  Dependencies: 1; dependents: 0.
- `@conformal_structure` — Metric structure modulo positive rescaling  
  Dependencies: 0; dependents: 0.
- `@conformal_compactification` — Finite representation of infinity  
  Dependencies: 0; dependents: 0.
- `@future_null_infinity` — Future endpoint of outgoing null curves  
  Dependencies: 0; dependents: 1.
- `@past_null_infinity` — Past endpoint of incoming null curves  
  Dependencies: 0; dependents: 0.
- `@causal_boundary` — Boundary encoding ideal causal endpoints  
  Dependencies: 0; dependents: 1.

## F3_CONNECTION_MOTION

- `@affine_connection` — Derivative operator on vector fields  
  Dependencies: 0; dependents: 1.
- `@levi_civita_connection` — Unique torsion-free metric-compatible connection  
  Dependencies: 1; dependents: 3.
- `@metric_compatibility` — Covariant constancy of metric  
  Dependencies: 1; dependents: 1.
- `@torsion_tensor` — Antisymmetric connection defect  
  Dependencies: 0; dependents: 0.
- `@christoffel_symbols` — Coordinate coefficients of a connection  
  Dependencies: 1; dependents: 1.
- `@covariant_derivative` — Connection-based tensor derivative  
  Dependencies: 1; dependents: 1.
- `@parallel_transport` — Connection-preserving transport along curves  
  Dependencies: 1; dependents: 1.
- `@geodesic` — Autoparallel extremal curve  
  Dependencies: 1; dependents: 2.
- `@geodesic_equation` — Second-order equation for affine geodesics  
  Dependencies: 2; dependents: 0.
- `@null_geodesic` — Geodesic with null tangent  
  Dependencies: 0; dependents: 1.
- `@timelike_geodesic` — Geodesic with timelike tangent  
  Dependencies: 0; dependents: 1.
- `@affine_parameter` — Parameter preserving geodesic equation form  
  Dependencies: 0; dependents: 0.
- `@exponential_map` — Map from tangent vectors to geodesics  
  Dependencies: 0; dependents: 0.
- `@normal_coordinates` — Coordinates with vanishing connection at a point  
  Dependencies: 0; dependents: 0.
- `@fermi_normal_coordinates` — Coordinates adapted to a timelike worldline  
  Dependencies: 0; dependents: 0.
- `@geodesic_deviation` — Relative acceleration of nearby geodesics  
  Dependencies: 2; dependents: 1.
- `@jacobi_field` — Linearized geodesic separation field  
  Dependencies: 1; dependents: 0.
- `@congruence` — Family of nonintersecting curves  
  Dependencies: 0; dependents: 1.
- `@null_congruence` — Congruence of null geodesics  
  Dependencies: 0; dependents: 0.
- `@timelike_congruence` — Congruence of timelike geodesics  
  Dependencies: 0; dependents: 0.
- `@expansion_scalar` — Fractional volume-rate of a congruence  
  Dependencies: 1; dependents: 1.
- `@shear_tensor` — Trace-free shape distortion  
  Dependencies: 1; dependents: 1.
- `@vorticity_tensor` — Rotation of a congruence  
  Dependencies: 1; dependents: 1.
- `@raychaudhuri_equation` — Evolution equation for congruence expansion  
  Dependencies: 2; dependents: 1.

## F4_CURVATURE

- `@riemann_tensor` — Curvature of the Levi-Civita connection  
  Dependencies: 2; dependents: 5.
- `@riemann_symmetries` — Algebraic symmetries of Riemann curvature  
  Dependencies: 0; dependents: 0.
- `@sectional_curvature` — Curvature assigned to tangent two-planes  
  Dependencies: 0; dependents: 0.
- `@ricci_tensor` — Trace of the Riemann tensor  
  Dependencies: 2; dependents: 4.
- `@ricci_scalar` — Metric trace of Ricci curvature  
  Dependencies: 2; dependents: 1.
- `@einstein_tensor` — Divergence-free curvature tensor  
  Dependencies: 3; dependents: 3.
- `@weyl_tensor` — Trace-free conformal curvature  
  Dependencies: 1; dependents: 1.
- `@schouten_tensor` — Ricci-derived conformal tensor  
  Dependencies: 0; dependents: 0.
- `@curvature_two_form` — Connection-curvature two-form  
  Dependencies: 0; dependents: 0.
- `@first_bianchi_identity` — Algebraic cyclic curvature identity  
  Dependencies: 1; dependents: 1.
- `@second_bianchi_identity` — Differential curvature identity  
  Dependencies: 1; dependents: 1.
- `@contracted_bianchi_identity` — Divergence-free Einstein tensor identity  
  Dependencies: 1; dependents: 1.
- `@kretschmann_scalar` — Quadratic Riemann invariant  
  Dependencies: 0; dependents: 0.
- `@pontryagin_scalar` — Parity-odd quadratic curvature invariant  
  Dependencies: 0; dependents: 0.
- `@petrov_classification` — Algebraic classification of Weyl curvature  
  Dependencies: 1; dependents: 0.
- `@newman_penrose_formalism` — Null-tetrad curvature formalism  
  Dependencies: 0; dependents: 0.
- `@tetrad` — Local frame field  
  Dependencies: 0; dependents: 0.
- `@spin_connection` — Connection on orthonormal/spin frames  
  Dependencies: 0; dependents: 0.

## F5_VARIATIONAL_FIELD_EQUATIONS

- `@einstein_hilbert_action` — Action integral of scalar curvature  
  Dependencies: 0; dependents: 1.
- `@matter_action` — Action for nongravitational fields  
  Dependencies: 0; dependents: 1.
- `@total_action` — Einstein-Hilbert plus matter action  
  Dependencies: 0; dependents: 0.
- `@metric_variation` — Variation with respect to inverse metric  
  Dependencies: 1; dependents: 1.
- `@boundary_term` — Boundary contribution from curvature variation  
  Dependencies: 0; dependents: 1.
- `@gibbons_hawking_york_term` — Boundary term for well-posed metric variation  
  Dependencies: 1; dependents: 0.
- `@stress_energy_tensor` — Metric variation of matter action  
  Dependencies: 1; dependents: 3.
- `@einstein_field_equation` — Curvature-matter field equation  
  Dependencies: 7; dependents: 5.
- `@vacuum_field_equation` — Einstein equation with vanishing stress-energy  
  Dependencies: 0; dependents: 2.
- `@cosmological_constant` — Constant curvature source term  
  Dependencies: 0; dependents: 1.
- `@local_energy_momentum_conservation` — Covariant conservation of stress-energy  
  Dependencies: 2; dependents: 1.
- `@diffeomorphism_invariance` — Gauge symmetry under smooth coordinate relabeling  
  Dependencies: 0; dependents: 0.
- `@noether_identity` — Identity generated by gauge symmetry  
  Dependencies: 0; dependents: 0.
- `@matter_coupling` — Coupling of geometry to stress-energy  
  Dependencies: 1; dependents: 1.
- `@trace_reversed_field_equation` — Ricci-form Einstein equation  
  Dependencies: 0; dependents: 0.
- `@energy_condition` — Restrictions on stress-energy contractions  
  Dependencies: 0; dependents: 0.
- `@null_energy_condition` — Nonnegative null contraction of stress-energy  
  Dependencies: 0; dependents: 2.
- `@weak_energy_condition` — Nonnegative energy density for timelike observers  
  Dependencies: 0; dependents: 0.
- `@strong_energy_condition` — Ricci-focusing condition for timelike observers  
  Dependencies: 0; dependents: 0.
- `@dominant_energy_condition` — Causal nonspacelike energy flux condition  
  Dependencies: 0; dependents: 0.

## F6_INITIAL_VALUE_ADM

- `@spacelike_hypersurface` — Codimension-one spacelike slice  
  Dependencies: 0; dependents: 1.
- `@induced_metric` — Riemannian metric on a spacelike slice  
  Dependencies: 1; dependents: 1.
- `@unit_normal` — Normalized normal to a hypersurface  
  Dependencies: 0; dependents: 0.
- `@extrinsic_curvature` — Embedding curvature of a slice  
  Dependencies: 1; dependents: 1.
- `@gauss_equation` — Relation between spacetime and hypersurface curvature  
  Dependencies: 0; dependents: 1.
- `@codazzi_equation` — Mixed curvature relation  
  Dependencies: 0; dependents: 1.
- `@adm_decomposition` — 3+1 spacetime decomposition  
  Dependencies: 1; dependents: 1.
- `@lapse_function` — Proper-time separation between slices  
  Dependencies: 1; dependents: 1.
- `@shift_vector` — Spatial relabeling between slices  
  Dependencies: 1; dependents: 1.
- `@hamiltonian_constraint` — Scalar constraint on initial data  
  Dependencies: 2; dependents: 1.
- `@momentum_constraint` — Vector constraint on initial data  
  Dependencies: 2; dependents: 1.
- `@evolution_equations` — ADM time evolution system  
  Dependencies: 1; dependents: 1.
- `@initial_data_set` — Spatial metric and extrinsic curvature with matter data  
  Dependencies: 0; dependents: 0.
- `@cauchy_problem` — Initial-value formulation of Einstein equations  
  Dependencies: 1; dependents: 1.
- `@maximal_cauchy_development` — Largest globally hyperbolic solution from data  
  Dependencies: 2; dependents: 1.
- `@constraint_propagation` — Preservation of constraints under evolution  
  Dependencies: 0; dependents: 0.
- `@gauge_condition` — Coordinate or hyperbolic reduction condition  
  Dependencies: 0; dependents: 0.
- `@harmonic_coordinates` — Coordinates satisfying wave equations  
  Dependencies: 0; dependents: 0.
- `@well_posedness` — Existence, uniqueness, and continuous dependence  
  Dependencies: 1; dependents: 0.

## F7_SYMMETRIES_CONSERVED

- `@isometry` — Metric-preserving diffeomorphism  
  Dependencies: 0; dependents: 1.
- `@killing_vector` — Generator of a continuous isometry  
  Dependencies: 2; dependents: 2.
- `@killing_equation` — Vanishing symmetrized covariant derivative  
  Dependencies: 1; dependents: 0.
- `@stationary_spacetime` — Spacetime with asymptotically timelike Killing field  
  Dependencies: 0; dependents: 0.
- `@static_spacetime` — Hypersurface-orthogonal stationary spacetime  
  Dependencies: 0; dependents: 0.
- `@axisymmetric_spacetime` — Spacetime with axial Killing field  
  Dependencies: 0; dependents: 0.
- `@komar_mass` — Mass integral from timelike Killing field  
  Dependencies: 1; dependents: 0.
- `@komar_angular_momentum` — Angular momentum integral from axial Killing field  
  Dependencies: 0; dependents: 0.
- `@adm_mass` — Total mass at spatial infinity  
  Dependencies: 1; dependents: 1.
- `@bondi_mass` — Retarded mass at null infinity  
  Dependencies: 1; dependents: 1.
- `@bondi_mass_loss` — Mass decrease by gravitational radiation  
  Dependencies: 1; dependents: 0.
- `@asymptotic_flatness` — Approach to Minkowski geometry at infinity  
  Dependencies: 0; dependents: 1.
- `@asymptotic_symmetry` — Symmetry preserving asymptotic structure  
  Dependencies: 0; dependents: 0.
- `@bms_group` — Asymptotic symmetry group at null infinity  
  Dependencies: 0; dependents: 0.
- `@noether_charge` — Covariant phase-space conserved charge  
  Dependencies: 0; dependents: 1.

## F8_LINEARIZED_GRAVITY_WAVES

- `@background_metric` — Reference exact solution  
  Dependencies: 0; dependents: 1.
- `@linear_metric_perturbation` — First-order perturbation of a background  
  Dependencies: 1; dependents: 1.
- `@gauge_transformation_linearized` — Infinitesimal diffeomorphism action on perturbation  
  Dependencies: 0; dependents: 1.
- `@trace_reversal` — Trace-adjusted perturbation  
  Dependencies: 1; dependents: 1.
- `@lorenz_gauge` — Divergence-free trace-reversed gauge  
  Dependencies: 1; dependents: 1.
- `@linearized_einstein_tensor` — First variation of Einstein tensor  
  Dependencies: 2; dependents: 1.
- `@linearized_field_equation` — First-order Einstein equation  
  Dependencies: 1; dependents: 1.
- `@vacuum_wave_equation` — Wave equation for vacuum perturbations  
  Dependencies: 1; dependents: 1.
- `@transverse_traceless_gauge` — Physical radiation gauge  
  Dependencies: 2; dependents: 1.
- `@spin_two_polarization` — Two helicity states of massless metric radiation  
  Dependencies: 1; dependents: 1.
- `@plus_polarization` — First tensor polarization  
  Dependencies: 0; dependents: 0.
- `@cross_polarization` — Second tensor polarization  
  Dependencies: 0; dependents: 0.
- `@geodesic_detector_response` — Relative displacement induced by a wave  
  Dependencies: 0; dependents: 0.
- `@quadrupole_formula` — Leading far-zone radiation formula  
  Dependencies: 1; dependents: 1.
- `@gravitational_wave` — Radiative spacetime curvature  
  Dependencies: 1; dependents: 2.
- `@gravitational_wave_energy_flux` — Effective radiation energy flux  
  Dependencies: 1; dependents: 1.
- `@memory_effect` — Permanent asymptotic displacement or symmetry transition  
  Dependencies: 0; dependents: 0.
- `@post_newtonian_expansion` — Weak-field slow-motion asymptotic expansion  
  Dependencies: 0; dependents: 0.
- `@binary_inspiral` — Radiation-driven orbital decay  
  Dependencies: 1; dependents: 1.
- `@merger` — Nonlinear coalescence phase  
  Dependencies: 1; dependents: 1.
- `@ringdown` — Quasinormal relaxation phase  
  Dependencies: 2; dependents: 0.

## F9_EXACT_SOLUTIONS

- `@minkowski_spacetime` — Flat Lorentzian spacetime  
  Dependencies: 0; dependents: 0.
- `@de_sitter_spacetime` — Maximally symmetric positive-curvature vacuum  
  Dependencies: 0; dependents: 0.
- `@anti_de_sitter_spacetime` — Maximally symmetric negative-curvature vacuum  
  Dependencies: 0; dependents: 0.
- `@schwarzschild_geometry` — Static spherical vacuum black-hole geometry  
  Dependencies: 1; dependents: 3.
- `@schwarzschild_radius` — Horizon radius in Schwarzschild geometry  
  Dependencies: 1; dependents: 1.
- `@birkhoff_theorem` — Uniqueness of spherical vacuum geometry  
  Dependencies: 0; dependents: 0.
- `@reissner_nordstrom_geometry` — Static charged black-hole geometry  
  Dependencies: 1; dependents: 0.
- `@kerr_geometry` — Rotating vacuum black-hole geometry  
  Dependencies: 1; dependents: 2.
- `@kerr_newman_geometry` — Rotating charged black-hole geometry  
  Dependencies: 1; dependents: 0.
- `@mass_parameter` — Asymptotic mass parameter  
  Dependencies: 0; dependents: 0.
- `@angular_momentum_parameter` — Rotation parameter  
  Dependencies: 0; dependents: 0.
- `@charge_parameter` — Electromagnetic charge parameter  
  Dependencies: 0; dependents: 0.
- `@boyer_lindquist_coordinates` — Standard Kerr coordinate system  
  Dependencies: 0; dependents: 0.
- `@eddington_finkelstein_coordinates` — Horizon-penetrating null coordinates  
  Dependencies: 0; dependents: 0.
- `@kruskal_szekeres_extension` — Maximal analytic Schwarzschild extension  
  Dependencies: 0; dependents: 0.
- `@maximal_extension` — Inextendible analytic spacetime completion  
  Dependencies: 0; dependents: 0.
- `@friedmann_lemaitre_robertson_walker_spacetime` — Homogeneous isotropic cosmological spacetime  
  Dependencies: 0; dependents: 1.
- `@vacuum_kasner_spacetime` — Anisotropic vacuum cosmology  
  Dependencies: 0; dependents: 0.

## F10_BLACK_HOLE_GEOMETRY

- `@black_hole_region` — Complement of causal past of future null infinity  
  Dependencies: 1; dependents: 2.
- `@event_horizon` — Boundary of black-hole region  
  Dependencies: 4; dependents: 3.
- `@apparent_horizon` — Outer boundary of trapped surfaces on a slice  
  Dependencies: 1; dependents: 0.
- `@trapping_horizon` — Hypersurface foliated by marginally trapped surfaces  
  Dependencies: 0; dependents: 0.
- `@killing_horizon` — Null hypersurface generated by a Killing field  
  Dependencies: 0; dependents: 1.
- `@isolated_horizon` — Quasilocal equilibrium horizon  
  Dependencies: 0; dependents: 0.
- `@dynamical_horizon` — Spacelike evolving horizon  
  Dependencies: 0; dependents: 0.
- `@ergoregion` — Region where stationary Killing field is spacelike  
  Dependencies: 1; dependents: 1.
- `@ergosphere` — Outer ergoregion boundary structure in Kerr  
  Dependencies: 1; dependents: 1.
- `@static_limit` — Surface where stationary Killing field becomes null  
  Dependencies: 1; dependents: 1.
- `@photon_sphere` — Spherical null orbit structure  
  Dependencies: 0; dependents: 1.
- `@light_ring` — Circular null geodesic  
  Dependencies: 0; dependents: 0.
- `@innermost_stable_circular_orbit` — Innermost stable timelike circular orbit  
  Dependencies: 0; dependents: 0.
- `@curvature_singularity` — Divergence or inextendibility of curvature structure  
  Dependencies: 0; dependents: 0.
- `@coordinate_singularity` — Coordinate failure without geometric singularity  
  Dependencies: 0; dependents: 0.
- `@ring_singularity` — Kerr curvature singularity  
  Dependencies: 0; dependents: 0.
- `@inner_horizon` — Cauchy horizon in charged or rotating solutions  
  Dependencies: 0; dependents: 0.
- `@cauchy_horizon` — Boundary of global predictability  
  Dependencies: 0; dependents: 0.
- `@surface_gravity` — Horizon inaffinity or redshift acceleration  
  Dependencies: 2; dependents: 3.
- `@horizon_area` — Area of a horizon cross-section  
  Dependencies: 1; dependents: 1.
- `@black_hole_mass` — Invariant/asymptotic mass of black hole  
  Dependencies: 0; dependents: 0.
- `@black_hole_angular_momentum` — Angular momentum of black hole  
  Dependencies: 0; dependents: 0.
- `@black_hole_charge` — Gauge charge of black hole  
  Dependencies: 0; dependents: 0.
- `@no_hair_theorem` — Stationary black-hole uniqueness characterization  
  Dependencies: 0; dependents: 0.
- `@black_hole_uniqueness` — Uniqueness of stationary electrovac black holes  
  Dependencies: 0; dependents: 0.
- `@cosmic_censorship` — Conjectured concealment/stability of singular behavior  
  Dependencies: 0; dependents: 0.

## F11_PENROSE_GLOBAL

- `@achronal_set` — Set with no timelike-related points  
  Dependencies: 0; dependents: 0.
- `@trapped_surface` — Compact spacelike surface with converging future null normals  
  Dependencies: 0; dependents: 2.
- `@closed_trapped_surface` — Compact boundaryless trapped surface  
  Dependencies: 0; dependents: 1.
- `@marginally_trapped_surface` — Surface with one vanishing null expansion  
  Dependencies: 0; dependents: 0.
- `@focusing_theorem` — Finite-parameter focusing under energy and vorticity conditions  
  Dependencies: 3; dependents: 1.
- `@conjugate_point` — Failure point of geodesic maximality  
  Dependencies: 1; dependents: 1.
- `@geodesic_incompleteness` — Existence of inextendible finite-affine-length geodesic  
  Dependencies: 1; dependents: 1.
- `@singularity_theorem` — Implication from global/energy/causal assumptions to incompleteness  
  Dependencies: 0; dependents: 0.
- `@penrose_singularity_theorem` — Null incompleteness from trapped surface and global assumptions  
  Dependencies: 3; dependents: 0.
- `@hawking_penrose_singularity_theorem` — Causal geodesic incompleteness under generic focusing conditions  
  Dependencies: 0; dependents: 0.
- `@generic_condition` — Curvature encountered nontrivially by geodesics  
  Dependencies: 0; dependents: 0.
- `@chronology_condition` — Absence of closed timelike curves  
  Dependencies: 0; dependents: 0.
- `@global_causal_structure` — Large-scale organization of causal relations  
  Dependencies: 0; dependents: 0.
- `@penrose_diagram` — Conformal causal diagram  
  Dependencies: 0; dependents: 0.
- `@singularity` — Boundary or incompleteness rather than ordinary point  
  Dependencies: 0; dependents: 0.

## F12_BLACK_HOLE_MECHANICS

- `@zeroth_law_black_hole_mechanics` — Constancy of surface gravity on stationary horizon  
  Dependencies: 1; dependents: 1.
- `@first_law_black_hole_mechanics` — Variational relation among mass, area, angular momentum, charge  
  Dependencies: 2; dependents: 1.
- `@second_law_black_hole_mechanics` — Nondecrease of horizon area classically  
  Dependencies: 1; dependents: 1.
- `@third_law_black_hole_mechanics` — Unattainability of zero surface gravity  
  Dependencies: 1; dependents: 0.
- `@area_theorem` — Classical horizon-area monotonicity  
  Dependencies: 1; dependents: 0.
- `@smarr_formula` — Scaling relation for stationary black holes  
  Dependencies: 0; dependents: 0.
- `@physical_process_first_law` — First law for perturbative matter infall  
  Dependencies: 0; dependents: 0.
- `@black_hole_mechanics` — Unified classical horizon laws  
  Dependencies: 0; dependents: 0.

## F13_QFT_CURVED

- `@quantum_field_in_curved_spacetime` — Quantum field theory on a fixed curved background  
  Dependencies: 0; dependents: 2.
- `@classical_field_equation` — Linear hyperbolic field equation on spacetime  
  Dependencies: 1; dependents: 1.
- `@klein_gordon_field` — Scalar field satisfying curved Klein-Gordon equation  
  Dependencies: 0; dependents: 0.
- `@solution_space` — Space of classical field solutions  
  Dependencies: 1; dependents: 1.
- `@symplectic_form` — Conserved antisymmetric form on solution space  
  Dependencies: 1; dependents: 1.
- `@complex_structure` — Positive-frequency splitting structure  
  Dependencies: 1; dependents: 1.
- `@field_operator` — Operator-valued distribution  
  Dependencies: 0; dependents: 0.
- `@canonical_commutation_relation` — Quantum algebra relation  
  Dependencies: 0; dependents: 0.
- `@mode_solution` — Normalized field-equation solution  
  Dependencies: 0; dependents: 0.
- `@mode_decomposition` — Expansion in positive and negative frequency modes  
  Dependencies: 1; dependents: 2.
- `@positive_frequency` — Observer/structure-dependent positive-energy splitting  
  Dependencies: 1; dependents: 1.
- `@negative_frequency` — Conjugate negative-frequency sector  
  Dependencies: 0; dependents: 0.
- `@fock_space` — Particle-number Hilbert-space representation  
  Dependencies: 0; dependents: 0.
- `@vacuum_state` — State annihilated by chosen annihilation operators  
  Dependencies: 1; dependents: 0.
- `@hadamard_state` — State with universal short-distance singularity  
  Dependencies: 0; dependents: 0.
- `@observer_dependent_particle` — Particle notion depending on mode splitting  
  Dependencies: 0; dependents: 0.
- `@bogoliubov_coefficient` — Overlap coefficients between mode bases  
  Dependencies: 1; dependents: 1.
- `@bogoliubov_transformation` — Canonical transformation between creation-annihilation bases  
  Dependencies: 1; dependents: 2.
- `@particle_creation` — Nonzero beta mixing between mode bases  
  Dependencies: 1; dependents: 1.
- `@unruh_effect` — Thermal response of uniformly accelerated detector  
  Dependencies: 0; dependents: 0.
- `@semiclassical_gravity` — Classical metric sourced by renormalized quantum stress-energy  
  Dependencies: 1; dependents: 1.
- `@renormalized_stress_energy_tensor` — Finite expectation value after covariant renormalization  
  Dependencies: 0; dependents: 1.
- `@backreaction` — Metric response to quantum expectation values  
  Dependencies: 1; dependents: 0.

## F14_HAWKING_THERMODYNAMICS

- `@hawking_temperature` — Thermal temperature set by surface gravity  
  Dependencies: 2; dependents: 1.
- `@hawking_radiation` — Asymptotic thermal particle flux from black holes  
  Dependencies: 4; dependents: 2.
- `@greybody_factor` — Frequency-dependent transmission through curvature potential  
  Dependencies: 1; dependents: 0.
- `@black_hole_evaporation` — Mass loss due to Hawking flux  
  Dependencies: 1; dependents: 1.
- `@evaporation_time` — Characteristic lifetime under semiclassical emission  
  Dependencies: 0; dependents: 0.
- `@bekenstein_hawking_entropy` — Quarter-area horizon entropy  
  Dependencies: 1; dependents: 1.
- `@black_hole_thermodynamics` — Thermodynamic interpretation of horizon mechanics  
  Dependencies: 1; dependents: 1.
- `@generalized_entropy` — Horizon entropy plus exterior entropy  
  Dependencies: 1; dependents: 2.
- `@generalized_second_law` — Nondecrease of generalized entropy  
  Dependencies: 1; dependents: 0.
- `@euclidean_periodicity` — Thermal periodicity of regular Euclidean section  
  Dependencies: 0; dependents: 0.
- `@tunneling_description` — Semiclassical horizon-crossing emission representation  
  Dependencies: 0; dependents: 0.
- `@hartle_hawking_state` — Thermal equilibrium state on eternal black hole  
  Dependencies: 0; dependents: 0.
- `@unruh_state` — Evaporating black-hole state regular on future horizon  
  Dependencies: 0; dependents: 0.
- `@boulware_state` — Static vacuum singular at horizon  
  Dependencies: 0; dependents: 0.

## F15_INFORMATION

- `@unitarity` — Norm-preserving quantum evolution  
  Dependencies: 0; dependents: 0.
- `@pure_state` — Rank-one quantum state  
  Dependencies: 0; dependents: 0.
- `@mixed_state` — Statistical density operator  
  Dependencies: 0; dependents: 0.
- `@density_matrix` — Positive unit-trace state operator  
  Dependencies: 0; dependents: 0.
- `@von_neumann_entropy` — Entropy of density matrix  
  Dependencies: 0; dependents: 1.
- `@entanglement_entropy` — Entropy from subsystem tracing  
  Dependencies: 0; dependents: 0.
- `@information_loss` — Apparent pure-to-mixed evolution  
  Dependencies: 0; dependents: 0.
- `@black_hole_information_problem` — Compatibility problem among evaporation, horizons, and unitarity  
  Dependencies: 2; dependents: 1.
- `@page_time` — Time near maximal radiation entropy  
  Dependencies: 0; dependents: 0.
- `@page_curve` — Expected entropy evolution under unitary evaporation  
  Dependencies: 2; dependents: 1.
- `@black_hole_complementarity` — Observer-dependent consistency proposal  
  Dependencies: 0; dependents: 0.
- `@firewall_problem` — Conflict among smooth horizon, unitarity, and monogamy  
  Dependencies: 0; dependents: 0.
- `@information_recovery` — Recovery of encoded information from radiation  
  Dependencies: 1; dependents: 0.
- `@island_formula` — Generalized entropy extremization including islands  
  Dependencies: 1; dependents: 1.
- `@quantum_extremal_surface` — Extremal generalized-entropy surface  
  Dependencies: 1; dependents: 0.

## F16_PERTURBATIONS_STABILITY

- `@black_hole_perturbation` — Linear/nonlinear deformation of a black-hole background  
  Dependencies: 0; dependents: 1.
- `@spherical_harmonic_decomposition` — Angular mode decomposition  
  Dependencies: 0; dependents: 0.
- `@tensor_harmonic_decomposition` — Tensor perturbation angular decomposition  
  Dependencies: 0; dependents: 0.
- `@regge_wheeler_equation` — Odd-parity Schwarzschild master equation  
  Dependencies: 2; dependents: 1.
- `@zerilli_equation` — Even-parity Schwarzschild master equation  
  Dependencies: 2; dependents: 1.
- `@teukolsky_equation` — Kerr spin-weighted master equation  
  Dependencies: 2; dependents: 1.
- `@master_variable` — Gauge-invariant perturbation variable  
  Dependencies: 0; dependents: 0.
- `@effective_potential` — One-dimensional scattering potential  
  Dependencies: 0; dependents: 2.
- `@quasinormal_mode` — Outgoing/ingoing dissipative eigenmode  
  Dependencies: 2; dependents: 2.
- `@quasinormal_frequency` — Complex mode frequency  
  Dependencies: 0; dependents: 0.
- `@linear_stability` — Boundedness and decay of linear perturbations  
  Dependencies: 0; dependents: 0.
- `@mode_stability` — Absence of exponentially growing separated modes  
  Dependencies: 0; dependents: 0.
- `@nonlinear_stability` — Orbital decay toward a nearby exact solution  
  Dependencies: 0; dependents: 0.
- `@price_law` — Late-time power-law tail  
  Dependencies: 0; dependents: 0.
- `@redshift_effect` — Horizon energy estimate mechanism  
  Dependencies: 0; dependents: 0.
- `@superradiance` — Rotational amplification of waves  
  Dependencies: 0; dependents: 0.
- `@mass_inflation` — Inner-horizon instability  
  Dependencies: 0; dependents: 0.

## F17_OBSERVABLES

- `@gravitational_lensing` — Null-geodesic image distortion  
  Dependencies: 0; dependents: 1.
- `@black_hole_shadow` — Lensed capture-region image  
  Dependencies: 2; dependents: 1.
- `@accretion_disk` — Radiating matter flow around compact object  
  Dependencies: 0; dependents: 0.
- `@redshift` — Frequency ratio from geometry and motion  
  Dependencies: 0; dependents: 0.
- `@shapiro_delay` — Gravitational null-propagation delay  
  Dependencies: 0; dependents: 0.
- `@perihelion_precession` — Relativistic orbital apsidal advance  
  Dependencies: 1; dependents: 0.
- `@light_deflection` — Curvature-induced null-geodesic bending  
  Dependencies: 1; dependents: 0.
- `@binary_pulsar_decay` — Observed radiation-reaction orbital decay  
  Dependencies: 0; dependents: 0.
- `@LIGO_observation` — Interferometric gravitational-wave observation  
  Dependencies: 1; dependents: 0.
- `@event_horizon_telescope` — Horizon-scale interferometric imaging  
  Dependencies: 1; dependents: 0.
- `@ringdown_observable` — Measured damped post-merger signal  
  Dependencies: 1; dependents: 0.
- `@shadow_observable` — Measured horizon-scale brightness depression  
  Dependencies: 0; dependents: 0.
- `@parameter_estimation` — Inference of source parameters from data  
  Dependencies: 0; dependents: 0.
- `@consistency_test_general_relativity` — Comparison of observations with GR predictions  
  Dependencies: 0; dependents: 0.

## F18_COSMOLOGY

- `@cosmology` — Global relativistic universe modeling  
  Dependencies: 2; dependents: 1.
- `@cosmological_principle` — Large-scale homogeneity and isotropy  
  Dependencies: 0; dependents: 0.
- `@scale_factor` — Relative size function in FLRW geometry  
  Dependencies: 1; dependents: 1.
- `@hubble_parameter` — Logarithmic expansion rate  
  Dependencies: 1; dependents: 1.
- `@friedmann_equation` — Hamiltonian cosmological evolution equation  
  Dependencies: 2; dependents: 1.
- `@acceleration_equation` — Second cosmological evolution equation  
  Dependencies: 1; dependents: 1.
- `@continuity_equation_cosmology` — Cosmological energy conservation  
  Dependencies: 1; dependents: 0.
- `@spatial_curvature_parameter` — Constant-curvature slice parameter  
  Dependencies: 0; dependents: 0.
- `@equation_of_state` — Pressure-density relation  
  Dependencies: 0; dependents: 0.
- `@cosmological_horizon` — Observer-dependent causal boundary in cosmology  
  Dependencies: 0; dependents: 0.
- `@particle_horizon` — Boundary of past causal contact  
  Dependencies: 0; dependents: 0.
- `@event_horizon_cosmology` — Boundary of future communicability  
  Dependencies: 0; dependents: 0.
- `@structure_formation` — Growth of cosmological inhomogeneity  
  Dependencies: 1; dependents: 1.
- `@primordial_black_hole` — Black hole formed in early-universe conditions  
  Dependencies: 1; dependents: 1.
- `@supermassive_black_hole` — High-mass black hole in galactic nucleus  
  Dependencies: 1; dependents: 1.
- `@galactic_nucleus` — Central galactic dynamical region  
  Dependencies: 0; dependents: 0.
- `@black_hole_cosmology` — Black holes embedded in cosmological evolution  
  Dependencies: 1; dependents: 0.

## Core equation registry

### EQ-GR-001 — Metric compatibility
Handle: `@metric_compatibility`
```text
∇_ρ g_{μν}=0
```

### EQ-GR-002 — Torsion
Handle: `@torsion_tensor`
```text
T^ρ_{μν}=Γ^ρ_{μν}-Γ^ρ_{νμ}
```

### EQ-GR-003 — Levi-Civita coefficients
Handle: `@christoffel_symbols`
```text
Γ^ρ_{μν}=1/2 g^{ρσ}(∂_μg_{νσ}+∂_νg_{μσ}-∂_σg_{μν})
```

### EQ-GR-004 — Affine geodesic equation
Handle: `@geodesic_equation`
```text
d²x^ρ/dλ²+Γ^ρ_{μν}(dx^μ/dλ)(dx^ν/dλ)=0
```

### EQ-GR-005 — Jacobi equation
Handle: `@geodesic_deviation`
```text
D²ξ^μ/dτ²=-R^μ_{ νρσ}u^νξ^ρu^σ
```

### EQ-GR-006 — Riemann curvature
Handle: `@riemann_tensor`
```text
R^ρ_{ σμν}=∂_μΓ^ρ_{νσ}-∂_νΓ^ρ_{μσ}+Γ^ρ_{μλ}Γ^λ_{νσ}-Γ^ρ_{νλ}Γ^λ_{μσ}
```

### EQ-GR-007 — Ricci contraction
Handle: `@ricci_tensor`
```text
R_{μν}=R^ρ_{ μρν}
```

### EQ-GR-008 — Scalar curvature
Handle: `@ricci_scalar`
```text
R=g^{μν}R_{μν}
```

### EQ-GR-009 — Einstein tensor
Handle: `@einstein_tensor`
```text
G_{μν}=R_{μν}-1/2 R g_{μν}
```

### EQ-GR-010 — Contracted Bianchi identity
Handle: `@contracted_bianchi_identity`
```text
∇^μG_{μν}=0
```

### EQ-GR-011 — Einstein-Hilbert action
Handle: `@einstein_hilbert_action`
```text
S_g=(c³/16πG)∫(R-2Λ)√(-g)d⁴x
```

### EQ-GR-012 — Stress-energy definition
Handle: `@stress_energy_tensor`
```text
T_{μν}=-(2/√(-g)) δS_m/δg^{μν}
```

### EQ-GR-013 — Einstein field equation
Handle: `@einstein_field_equation`
```text
G_{μν}+Λg_{μν}=(8πG/c⁴)T_{μν}
```

### EQ-GR-014 — Covariant conservation
Handle: `@local_energy_momentum_conservation`
```text
∇_μT^{μν}=0
```

### EQ-GR-015 — Timelike Raychaudhuri equation
Handle: `@raychaudhuri_equation`
```text
dθ/dτ=-(1/3)θ²-σ_{μν}σ^{μν}+ω_{μν}ω^{μν}-R_{μν}u^μu^ν
```

### EQ-GR-016 — Null Raychaudhuri equation
Handle: `@raychaudhuri_equation`
```text
dθ/dλ=-(1/2)θ²-σ_{μν}σ^{μν}+ω_{μν}ω^{μν}-R_{μν}k^μk^ν
```

### EQ-GR-017 — Hamiltonian constraint
Handle: `@hamiltonian_constraint`
```text
³R+K²-K_{ij}K^{ij}=16πGρ/c⁴+2Λ
```

### EQ-GR-018 — Momentum constraint
Handle: `@momentum_constraint`
```text
D_j(K^{ij}-γ^{ij}K)=8πG j^i/c⁴
```

### EQ-GR-019 — Killing equation
Handle: `@killing_equation`
```text
∇_{(μ}ξ_{ν)}=0
```

### EQ-GR-020 — Metric expansion
Handle: `@linear_metric_perturbation`
```text
g_{μν}=ḡ_{μν}+h_{μν}+O(h²)
```

### EQ-GR-021 — Trace reversal
Handle: `@trace_reversal`
```text
h̄_{μν}=h_{μν}-1/2 ḡ_{μν}h
```

### EQ-GR-022 — Lorenz gauge
Handle: `@lorenz_gauge`
```text
∇̄^μh̄_{μν}=0
```

### EQ-GR-023 — Flat-background wave equation
Handle: `@vacuum_wave_equation`
```text
□h̄_{μν}=0
```

### EQ-GR-024 — Quadrupole waveform
Handle: `@quadrupole_formula`
```text
h^{TT}_{ij}(t,r)=(2G/c⁴r) d²Q^{TT}_{ij}(t-r/c)/dt²
```

### EQ-GR-025 — Bondi mass loss
Handle: `@bondi_mass_loss`
```text
dM_B/du=-(1/32πG)∫N_{AB}N^{AB}dΩ
```

### EQ-GR-026 — Schwarzschild line element
Handle: `@schwarzschild_geometry`
```text
ds²=-(1-2GM/c²r)c²dt²+(1-2GM/c²r)^{-1}dr²+r²dΩ²
```

### EQ-GR-027 — Schwarzschild radius
Handle: `@schwarzschild_radius`
```text
r_s=2GM/c²
```

### EQ-GR-028 — Reissner-Nordström lapse
Handle: `@reissner_nordstrom_geometry`
```text
f(r)=1-2GM/(c²r)+GQ²/(4πε₀c⁴r²)
```

### EQ-GR-029 — Kerr horizon radii
Handle: `@kerr_geometry`
```text
r_±=GM/c²±√((GM/c²)²-a²)
```

### EQ-GR-030 — Schwarzschild Kretschmann scalar
Handle: `@kretschmann_scalar`
```text
K=R_{αβγδ}R^{αβγδ}=48G²M²/(c⁴r⁶)
```

### EQ-GR-031 — Killing-horizon surface gravity
Handle: `@surface_gravity`
```text
χ^ν∇_νχ^μ=κχ^μ on H
```

### EQ-GR-032 — First law
Handle: `@first_law_black_hole_mechanics`
```text
δM=(κ/8πG)δA+Ω_HδJ+Φ_HδQ
```

### EQ-GR-033 — Smarr relation
Handle: `@smarr_formula`
```text
M=κA/(4πG)+2Ω_HJ+Φ_HQ
```

### EQ-GR-034 — Classical area monotonicity
Handle: `@area_theorem`
```text
dA_H/dλ≥0
```

### EQ-GR-035 — Curved Klein-Gordon equation
Handle: `@klein_gordon_field`
```text
(□_g+m²+ξR)φ=0
```

### EQ-GR-036 — Canonical commutation relation
Handle: `@canonical_commutation_relation`
```text
[a_i,a_j†]=δ_{ij}
```

### EQ-GR-037 — Bogoliubov mode transform
Handle: `@bogoliubov_transformation`
```text
u'_i=Σ_j(α_{ij}u_j+β_{ij}u_j*)
```

### EQ-GR-038 — Created particle number
Handle: `@particle_creation`
```text
⟨N_i⟩=Σ_j|β_{ij}|²
```

### EQ-GR-039 — Hawking temperature
Handle: `@hawking_temperature`
```text
T_H=ħκ/(2πk_B c)
```

### EQ-GR-040 — Bekenstein-Hawking entropy
Handle: `@bekenstein_hawking_entropy`
```text
S_BH=k_B c³A/(4Għ)
```

### EQ-GR-041 — Approximate Schwarzschild mass loss
Handle: `@black_hole_evaporation`
```text
dM/dt≈-ħc⁴/(15360πG²M²)
```

### EQ-GR-042 — Approximate lifetime
Handle: `@evaporation_time`
```text
t_evap≈5120πG²M³/(ħc⁴)
```

### EQ-GR-043 — Von Neumann entropy
Handle: `@von_neumann_entropy`
```text
S(ρ)=-Tr(ρ log ρ)
```

### EQ-GR-044 — Generalized entropy
Handle: `@generalized_entropy`
```text
S_gen=A/(4Għ)+S_out
```

### EQ-GR-045 — Island formula
Handle: `@island_formula`
```text
S(R)=min_ext[(Area(∂I)/(4Għ))+S_bulk(R∪I)]
```

### EQ-GR-046 — Regge-Wheeler master equation
Handle: `@regge_wheeler_equation`
```text
(∂²_{r_*}-∂²_t-V_RW)Ψ_RW=0
```

### EQ-GR-047 — Zerilli master equation
Handle: `@zerilli_equation`
```text
(∂²_{r_*}-∂²_t-V_Z)Ψ_Z=0
```

### EQ-GR-048 — Teukolsky master equation
Handle: `@teukolsky_equation`
```text
𝒯_s[ψ_s]=0
```

### EQ-GR-049 — Quasinormal time dependence
Handle: `@quasinormal_mode`
```text
Ψ∼e^{-iωt}, Im(ω)<0
```

### EQ-GR-050 — First Friedmann equation
Handle: `@friedmann_equation`
```text
H²=(8πG/3)ρ-kc²/a²+Λc²/3
```

### EQ-GR-051 — Acceleration equation
Handle: `@acceleration_equation`
```text
ä/a=-(4πG/3)(ρ+3p/c²)+Λc²/3
```

### EQ-GR-052 — Cosmological continuity
Handle: `@continuity_equation_cosmology`
```text
ρ̇+3H(ρ+p/c²)=0
```

## Closure boundary

The graph is complete for the Constitution's **General Relativity Minimal Complete Closure** target: it contains the foundations required to define spacetime, recover connection and curvature, derive the Einstein tensor and field equations, formulate the initial-value problem, recover exact black-hole geometries and global causal structure, enter quantum field theory in curved spacetime, recover Hawking radiation and black-hole thermodynamics, represent perturbations and observations, and connect the branch to cosmology.

Open research frontiers are preserved as unresolved boundaries rather than treated as missing foundational dependencies:
- full nonlinear stability of generic Kerr in complete generality
- strong cosmic censorship in all matter/cosmological regimes
- weak cosmic censorship in full generality
- complete quantum-gravity resolution of evaporation
- final resolution of the black-hole information problem
- derivation of MK43 native-to-readable projection from accepted GR alone