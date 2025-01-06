#
# C O N S T A N T S
#
from enum import Enum

# General things
DELIMETER = "_"
DASH = "-"

# UI
UI_STATUS_OK = "OK"
UI_STATUS_NOT_OK = "Not OK"
UI_STATUS_UNKNOWN = "Unknown"
UI_OPERATION_IMAGING = "Imaging only"
UI_OPERATION_WEEDING = "Weeding"
UI_OPERATION_NONE = "No operation in progress"
UI_CONFIRM_IMAGING_ALL_OK = "Begin Imaging?"
UI_CONFIRM_IMAGING_WITH_ERRORS = "Not all components are operational. Do you want to begin imaging?"

# File names
VECTOR = "vector"
PREFIX_CAMERA_CONFIGURATION = "camera-configuration-"
PREFIX_IMAGE = "img-"
EXTENSION_CAMERA_SETTINGS = ".pfs"
EXTENSION_IMAGE = ".jpg"
EXTENSION_PNG = ".png"
EXTENSION_NPY = ".npy"
EXTENSION_NPZ = ".npz"
EXTENSION_META = ".meta"
EXTENSION_CSV = ".csv"
EXTENSION_HTML = ".html"

FILENAME_POST_EMITTER = "post-emitter"
FILENAME_RAW = "raw"
FILENAME_FINISHED = "finished"
FILENAME_PROCESSED = "processed"
FILENAME_ORIGINAL = "segmented"
FILENAME_INTEL_RGB = "rgb"
FILENAME_INTEL_DEPTH = "depth"
FILENAME_DUMMY = "dummy"
FILENAME_NORMALIZED = "normalized"
FILENAME_DATAFRAME = "dataframe"
FILENAME_DETAILS = "details.txt"

IP_NONE = "NONE"

# This is just the text that will be placed on the visible treatment plan
SPRAYER_NAME = ""

THREAD_NAME_ODOMETRY        = "odometry"
THREAD_NAME_SYSTEM          = "system"
THREAD_NAME_TREATMENT       = "treatment"
THREAD_NAME_ACQUIRE         = "acquire"
THREAD_NAME_ACQUIRE_POST    = "acquire_post"
THREAD_NAME_ACQUIRE_RGB     = "acquireIntel"
THREAD_NAME_DIAGNOSTICS     = "diagnostics"
THREAD_NAME_REQ_RSP         = "reqrsp"
THREAD_NAME_SERVICE         = "service"
THREAD_NAME_HOUSEKEEPING    = "housekeeping"
THREAD_NAME_IMU             = "imu"
THREAD_NAME_DEPTH           = "depth"
THREAD_NAME_GPS             = "gps"
# These next two are temporary -- not needed when we move the depth cameras to the jetson
THREAD_NAME_DEPTH_LEFT      = "depth_left"
THREAD_NAME_DEPTH_RIGHT     = "depth_right"
THREAD_NAME_POSITION        = "position"
THREAD_NAME_SUPERVISOR      = "supervisor"
THREAD_NAME_ENRICH          = "enrich"
THREAD_NAME_UPDATE          = "update"

MSG_NOT_CONNECTED = "Not connected"
MSG_LINES_NOT_SPECIFIED = "The A and B lines for the odometer must be on the command line or in the INI file"
MSG_ODOMETER_CONNECTION = "Could not connect to odometer"

MSG_NO_PROBLEM_FOUND = "No problem found"

# Names for the attributes
# Some of these are a bit redundant and are there for backwards compatibility
NAME_BLOB                   = "blob"
NAME_AREA                   = "area"
NAME_TYPE                   = "type"
NAME_ACTUAL                 = "actual"
NAME_LOCATION               = "location"
NAME_CIELAB_L               = "cie_l"
NAME_CIELAB_A               = "cie_a"
NAME_CIELAB_B               = "cie_b"
NAME_CENTER                 = "center"
NAME_CONTOUR                = "contour"
NAME_BOX_DIMENSIONS         = "dimensions"
NAME_SHAPE_INDEX            = "shape_index"
NAME_RATIO                  = "lw_ratio"
NAME_IMAGE                  = "image"
NAME_GREYSCALE_IMAGE        = "greyscale"
NAME_REASON                 = "reason"
NAME_SIZE_RATIO             = "size_ratio"
NAME_BLUE                   = "blue"
NAME_GREEN                  = "green"
NAME_RED                    = "red"
NAME_DISTANCE               = "distance"
NAME_DISTANCE_NORMALIZED    = "normalized_distance"
NAME_AGL                    = "agl"
NAME_NAME                   = "name"
NAME_NUMBER                 = "number"
NAME_HEIGHT                 = "height"
NAME_NEIGHBOR_COUNT         = "neighbors"
NAME_HUE                    = "hue"
NAME_HUE_MEAN               = "hue_mean"
NAME_HUE_STDDEV             = "hue_stddev"
NAME_SATURATION             = "saturation_mean"
NAME_HSI                    = "hsi"
NAME_HSI_INTENSITY          = "hsi_intensity"
NAME_HSI_SATURATION         = "hsi_saturation"
NAME_HSI_HUE                = "hsi_hue"
NAME_HSV_HUE                = "hsv_hue"
NAME_HSV_SATURATION         = "hsv_saturation"
NAME_HSV_VALUE              = "value"
NAME_SATURATION_STDEV       = "saturation_stddev"
NAME_YIQ                    = "yiq"
NAME_I_YIQ                  = "in_phase"
NAME_I_MEAN                 = "in_phase_mean"
NAME_I_STDDEV               = "in_phase_stddev"
NAME_Q_MEAN                 = "quadrature_mean"
NAME_Q_STDDEV               = "quadrature_stddev"
NAME_BLUE_DIFFERENCE        = "cb_mean"
NAME_BLUE_DIFFERENCE_MEAN   = "cb_mean"
NAME_BLUE_DIFFERENCE_STDEV  = "cb_stddev"
NAME_RED_DIFFERENCE_MEAN    = "cr_mean"
NAME_RED_DIFFERENCE_STDEV   = "cr_stddev"
NAME_CONVEX_HULL            = "hull"
NAME_COMPACTNESS            = "compactness"
NAME_ELONGATION             = "elongation"
NAME_ECCENTRICITY           = "eccentricity"
NAME_ROUNDNESS              = "roundness"
NAME_CONVEXITY              = "convexity"
NAME_SOLIDITY               = "solidity"
NAME_DIST_TO_LEADING_EDGE   = "leading"
NAME_SQUARES                = "squares"
NAME_YCBCR_LUMA             = "ycbcr_y"
NAME_YCBCR_BLUE_DIFFERENCE  = "ycbcr_cb"
NAME_YCBCR_RED_DIFFERENCE   = "ycbcr_cr"
NAME_YIQ_Y                  = "yiq_y"
NAME_YIQ_I                  = "yiq_i"
NAME_YIQ_Q                  = "yiq_q"
NAME_CROP                   = "crop"
NAME_WEED                   = "weed"
NAME_MISTAKE                = "mistake"
NAME_BOUNDARY_CHAIN         = "chain"
NAME_BENDING                = "bending"
NAME_KSLOPE                 = "kslope"
NAME_KCURVATURE_APPROXIMATE = "kcurvature_approximate"
NAME_KCURVATURE             = "kcurvature"
NAME_ABSCURVATURE           = "abscurvature"
NAME_RADIAL_DISTANCE        = "radial"
NAME_RADIAL_AVG             = "radial_avg"
NAME_RADIAL_VAR             = "radial_var"
NAME_RADIAL_NORM            = "radial_normalized"
NAME_RADIAL_CROSSINGS_PCT   = "radial_crossing"


NAME_IMAGE_GREYSCALE        = "greyscale"
NAME_IMAGE_YIQ              = "yiq"
NAME_IMAGE_RGB              = "rgb"
NAME_IMAGE_HSV              = "hsv"
NAME_IMAGE_HSI              = "hsi"
NAME_IMAGE_YCBCR            = "ycbcr"
NAME_IMAGE_CIELAB           = "cielab"



# Column names in pandas
COLUMN_NAME_VALUE           = "value"
COLUMN_NAME_SUBTYPE         = "subtype"
COLUMN_NAME_TYPE            = "type"
COLUMN_NAME_FACTOR          = "factor"
COLUMN_NAME_KIND            = "kind"

# B A N D S
# The band names -- used for GLCM computations
NAME_GREYSCALE              = "greyscale"

# G L C M
NAME_ENERGY                 = "energy"
NAME_ENTROPY                = "entropy"
NAME_CORRELATION            = "correlation"
NAME_DISSIMILARITY          = "dissimilarity"
NAME_HOMOGENEITY            = "homogeneity"
NAME_CONTRAST               = "contrast"
NAME_ASM                    = "ASM"
NAME_AVERAGE                = "avg"

# H O G
KEYWORD_IMAGE               = "image"
NAME_HOG                    = "hog"

NAME_STDDEV                 = "stddev"
NAME_MEAN                   = "mean"
NAME_VAR                    = "variance"

# P R O X I M I T Y
NAME_PROXIMITY              = "proximity"
NAME_LID                    = "lid"
NAME_STICKER                = "sticker"

# L B P
NAME_LBP                    = "lbp"

#
# X M P P  R O O M S  A N D  J I D S
#
CONFERENCE_DNS              = "conference.weeds.com"
ROOM_ODOMETRY               = "odometry" + "@" + CONFERENCE_DNS
ROOM_TREATMENT              = "treatment" + "@" + CONFERENCE_DNS
ROOM_SYSTEM                 = "system" + "@" + CONFERENCE_DNS


# TODO: There are two Jetsons in the system. We need a scheme for controller-1@weeds.local and controller-2.weeds.local

JID_ODOMETRY                = "rio@weeds.com"
JID_RIO                     = "rio@weeds.com"
JID_JETSON                  = "controller@weeds.com"
JID_JETSON_1                = "jetson1@weeds.com"
JID_JETSON_2                = "jetson2@weeds.com"
JID_CONSOLE                 = "console@weeds.com"


DEFAULT_PASSWORD            = "greydog"
#DEFAULT_PASSWORD           = "weeds"

NICK_CONTROLER              = "controller"
NICK_ODOMETRY               = "rio"
NICK_TREATMENT              = "treatment"
NICK_JETSON                 = "jetson"
NICK_JETSON_1               = "left"
NICK_JETSON_2               = "right"
NICK_CONSOLE                = "console"
MSG_TYPE_NORMAL             = "normal"
MSG_TYPE_GROUPCHAT          = "groupchat"

# The timeout period for the processing
PROCESS_TIMEOUT             = 10000.0
PROCESS_TIMEOUT_LONG        = 10000.0
PROCESS_TIMEOUT_SHORT       = 4.0
KEYWORD_TIMEOUT             = "TIMEOUT"

# Temporary
NAME_CROP_SCORE = "score"

# A shortcut used for the command line
NAME_ALL = "all"
NAME_NONE = "none"

#
# R I O
#
RIO_TASK_NAME = "readEncoder"

#
# I M A G E S
#
# Image acquisition strategy
STRATEGY_ASYNC = 0
STRATEGY_SYNC = 1

# The number of images to keep
IMAGE_QUEUE_LEN = 20
DEPTH_QUEUE_LEN = 8
# Probably way too long 5000 ms for camera to acquire image
TIMEOUT_CAMERA = 5000

KEYWORD_DIRECTORY = "directory"
KEYWORD_IP = "ip"
KEYWORD_FILE_GYRO = "gyro"
KEYWORD_FILE_ACCELERATION = "acceleration"
KEYWORD_SERIAL = "serial"
KEYWORD_CONFIGURATION = "config"
KEYWORD_CAPTURE_STRATEGY = "capture"
KEYWORD_IMAGE_EVENTS = "image"
KEYWORD_CONFIGURATION_EVENTS = "configuration"

KEYWORD_BEGIN_AGL = "begin_agl"
KEYWORD_END_AGL = "end_agl"
KEYWORD_BEGIN_DATE = "begin_date"
KEYWORD_END_DATE = "end_date"
KEYWORD_CROP = "crop"
KEYWORD_ML_TECHNIQUE = "ml"
KEYWORD_PARENT = "parent"

KEYWORD_OUTPUT = "output"

CAPTURE_STRATEGY_QUEUED = "queued"
CAPTURE_STRATEGY_LIVE = "live"

PARAM_FILE_GYRO = "gyro.csv"
PARAM_FILE_ACCELERATION = "acceleration.csv"

#
# D E P T H
#
DEPTH_MAX_HORIZONTAL = 1280
DEPTH_MAX_VERTICAL = 720
DEPTH_MAX_FRAMES = 30

#
# I N T E L  R G B
# Max for camera is 1920x1080x8
# The higher stream value does work, but when it streams both depth and rgb, the resolution must match so the images
# can be aligned, presumably.
# So if we decide not to use the depth data, this can go to 1920x1080x8
INTEL_RGB_MAX_HORIZONTAL = 1280
INTEL_RGB_MAX_VERTICAL = 720
INTEL_RGB_MAX_FRAMES = 30

#
# I M U
#
# The files that will hold the IMU information for the weeding session

FILE_GYRO = "gyro.csv"
FILE_ACCELERATION = "acceleration.csv"
FILE_DEPTH = "depth-{:03d}.npy"

names = [NAME_AREA, NAME_TYPE, NAME_LOCATION, NAME_CENTER, NAME_CONTOUR, NAME_SHAPE_INDEX, NAME_RATIO, NAME_IMAGE, NAME_REASON, NAME_HUE_MEAN, NAME_SATURATION]

# REASONS why things were scored the way they were
REASON_UNKNOWN = 0
REASON_AT_EDGE = 1
REASON_SIZE_RATIO = 2
REASON_LOGISTIC_REGRESSION = 3
REASON_KNN = 4
REASON_DECISION_TREE = 5
REASON_RANDOM_FOREST = 6
REASON_GRADIENT = 7
REASON_SVM = 8
REASON_LDA = 9
REASON_MLP = 10
REASON_EXTRA = 11
REASON_TOO_CLOSE = 11
REASONS = ["Unknown", "At Edge", "Size", "Logistic", "KNN", "Decision Tree", "Random Forest", "Gradient", "SVM", "LDA", "MLP", "EXTRA", "Too Close"]

# TYPES of vegetation
TYPE_DESIRED = 0
TYPE_UNDESIRED = 1
TYPE_UNTREATED = 2
TYPE_IGNORED = 3
TYPE_UNKNOWN = 4
TYPES = ["Desired", "Undesired", "Untreated", "Ignored", "Unknown"]

TYPE_CROP = TYPE_DESIRED
TYPE_WEED = TYPE_UNDESIRED
TYPE_MISTAKE = TYPE_IGNORED

# Items contained in performance csv for analysis

PERF_ANGLES     = "angles"
PERF_ACQUIRE_BASLER_RGB = "acquire-basler"
PERF_ACQUIRE_INTEL_RGB  = "acquire-intel-rgb"
PERF_CIELAB     = "cielab"
PERF_CLASSIFY   = "classify"
PERF_CONTOURS   = "contours"
PERF_DISTANCE   = "distance"
PERF_INDEX      = "index"
PERF_LW_RATIO   = "LWRatio"
PERF_OVERLAP    = "overlap"
PERF_REGRESSION = "regression"
PERF_SHAPES_IDX = "shapes_idx"
PERF_TREATMENT  = "treatment"
PERF_COLORS     = "colors"
PERF_HSI        = "hsi"
PERF_HSV        = "hsv"
PERF_YIQ        = "yiq"
PERF_YCC        = "ycc"
PERF_MEAN       = "mean"
PERF_MEAN_SAT   = "mean-saturation"
PERF_MEAN_HUE   = "mean-hue"
PERF_MEAN_DIFF  = "mean-blue-diff"
PERF_STDDEV_YIQ = "stddev-yiq"
PERF_COMPACTNESS= "compactness"
PERF_SHAPES     = "shapes"
PERF_UNDISTORT  = "undistort"
PERF_GLCM       = "glcm"
PERF_HOG        = "hog"
PERF_LBP        = "lbp"

PERF_GLCM_GREYSCALE = "glcm-greyscale"
PERF_GLCM_YIQ_Y = "glcm-yiq-y"
PERF_GLCM_YIQ_I = "glcm-yiq-i"
PERF_GLCM_YIQ_Q = "glcm-yiq-q"
PERF_GLCM_HSV_H = "glcm-hsv-h"
PERF_GLCM_HSV_S = "glcm-hsv-s"
PERF_GLCM_HSV_V = "glcm-hsv-v"
PERF_GLCM_RGB_R = "glcm-rgb-r"
PERF_GLCM_RGB_G = "glcm-rgb-g"
PERF_GLCM_RGB_B = "glcm-rgb-b"
PERF_GLCM_HSI_H = "glcm-hsv-h"
PERF_GLCM_HSI_S = "glcm-hsv-s"
PERF_GLCM_HSI_I = "glcm-hsv-i"
PERF_GLCM_YCBCR_Y  = "glcm-ycbcr-y"
PERF_GLCM_YCBCR_CB = "glcm-ycbcr-cb"
PERF_GLCM_YCBCR_CR = "glcm-ycbcr-cr"
PERF_GLCM_CIELAB_L = "glcm-cielab-l"
PERF_GLCM_CIELAB_A = "glcm-cielab-a"
PERF_GLCM_CIELAB_B = "glcm-cielab-b"


PERF_SAVE_INTEL_DEPTH       = "save-intel-depth"
PERF_SAVE_INTEL_RGB         = "save-intel-rgb"
PERF_SAVE_INTEL_RGB_NPY     = "save-intel-rgb-npy"
PERF_SAVE_BASLER_RGB        = "save-basler"
PERF_TREATMENT_MSG          = "treatment-msg"

PERF_TITLE_ACTIVITY = "activity"
PERF_TITLE_MILLISECONDS = "milliseconds"
PERF_TITLE_MICROSECONDS = "microseconds"

COLOR_TREATMENT_GRID = (0, 255, 0)
COLOR_TREATMENT_WEED = (0, 0, 255)
COLOR_TREATMENT_SPRAYER_ON = (0, 0, 255)
COLOR_TREATMENT_SPRAYER_OFF = (0, 0, 255)
SIZE_TREATMENT_LINE = 4
# Originally 5
SIZE_CONTOUR_LINE = 5

# Properties
PROPERTY_SECTION_DATABASE = "DATABASE"
PROPERTY_HOST = "HOST"
PROPERTY_PORT = "PORT"
PROPERTY_DB = "NAME"
PROPERTY_DNS_SERVER = "DNS"
PROPERTY_LOGGING_FILENAME = "logging.ini"
PROPERTY_DISTANCE_TIER = "DISTANCE-TIERS"
PROPERTY_DISTANCE_EMITTERS = "DISTANCE-EMITTERS"
PROPERTY_FILENAME = "options.ini"
PROPERTY_FILENAME_FINISHED = "FINISHED"
PROPERTY_PIXELS_PER_MM = "PIXELS-PER-MM"
PROPERTY_SECTION_CAMERA = "CAMERA"
PROPERTY_SECTION_IMAGE_PROCESSING = "IMAGE-PROCESSING"
PROPERTY_SECTION_INTEL = "INTEL"
PROPERTY_CAPTURE = "CAPTURE"
PROPERTY_SECTION_EMITTER = "EMITTERS"
PROPERTY_SECTION_POST_EMITTER = "POST-EMITTER"
PROPERTY_CAMERA_IP = "IP" #"169.254.212.41"
PROPERTY_CAMERA_IP_POST = "POST-EMITTER-IP"
PROPERTY_DEPTH_WIDTH = "IMAGE_WIDTH"
PROPERTY_DEPTH_HEIGHT = "IMAGE_HEIGHT"
PROPERTY_IMAGE_WIDTH = "IMAGE_WIDTH"
PROPERTY_FACTORS = "FACTORS"
PROPERTY_IMAGE_HEIGHT = "IMAGE_HEIGHT"
PROPERTY_OFFSET_X = "EMITTER-X-OFFSET"
PROPERTY_OFFSET_Y = "EMITTER-Y-OFFSET"
PROPERTY_OVERLAP_FACTOR = "OVERLAP_FACTOR"
PROPERTY_RESOLUTION = "RESOLUTION"
PROPERTY_OUTPUT = "OUTPUT"
PROPERTY_SERIAL = "SERIAL"
PROPERTY_LOCATION = "LOCATION"
# Temporary until the depth cameras are moved to the NVIDIA systems
PROPERTY_SERIAL_LEFT = "SERIAL-LEFT"
PROPERTY_SERIAL_RIGHT = "SERIAL-RIGHT"

# I M A G E  P R O C E S S I N G
PROPERTY_FACTOR_COLOR = "color"
PROPERTY_FACTOR_GLCM = "glcm"
PROPERTY_FACTOR_LBP = "lbp"
PROPERTY_FACTOR_POSITION = "position"
PROPERTY_FACTOR_SHAPE = "shape"
PROPERTY_FACTOR_TEXTURE = "texture"


# D E P T H
PROPERTY_SECTION_DEPTH = "DEPTH"
PROPERTY_AGL_UP = "AGL_UP"
PROPERTY_AGL_DOWN = "AGL_DOWN"
PROPERTY_AGL_STOP = "AGL_STOP"
PROPERTY_EXPOSURE = "EXPOSURE"
DEFAULT_EXPOSURE = 9.0

# R I O
PROPERTY_SECTION_RIO = "RIO"
PROPERTY_RIGHT = "RIGHT-9403"
PROPERTY_LEFT = "LEFT-9403"
PROPERTY_CARD_ODOMETER = "NAME-9411"

# O D O M E T E R
PROPERTY_SECTION_ODOMETER = "ODOMETER"
PROPERTY_FORWARD = "FORWARD"
PROPERTY_LINE_A = "LINE-A"
PROPERTY_LINE_B = "LINE-B"
PROPERTY_LINE_Z = "LINE-Z"
PROPERTY_PFI_A = "PFI-A"
PROPERTY_PFI_B = "PFI-B"
PROPERTY_PFI_Z = "PFI-Z"
PROPERTY_PPR = "PULSES"
PROPERTY_COUNTER = "COUNTER"
PROPERTY_WHEEL_CIRCUMFERENCE = "WHEEL-SIZE"
PROPERTY_ENCODER_TYPE = "TYPE"
PROPERTY_DEBOUNCE = "DEBOUNCE"
PROPERTY_ANNOUNCEMENTS = "ANNOUNCEMENTS"

# Things that will be passed in keyword arguments
KEYWORD_ALTITUDE = "ALTITUDE"
KEYWORD_COM = "COM"
KEYWORD_DATE_BEGIN = "BEGIN"
KEYWORD_DATE_END = "END"
KEYWORD_LINE_A = "LINE_A"
KEYWORD_LINE_B = "LINE_B"
KEYWORD_WHEEL_CIRCUMFERENCE = "WHEEL_SIZE"
KEYWORD_PPR = "PULSES"
KEYWORD_SPEED = "SPEED"
KEYWORD_COUNTER = "COUNTER"
KEYWORD_FORWARD = "FORWARD"
KEYWORD_GSD = "GSD"
KEYWORD_CALLBACK = "CALLBACK"
KEYWORD_TYPE = "TYPE"
KEYWORD_EXPOSURE = "EXPOSURE"
KEYWORD_LAT = "LATITUDE"
KEYWORD_LONG = "LONGITUDE"
KEYWORD_PULSES = "PULSES"
KEYWORD_SOFTWARE = "SOFTWARE"
KEYWORD_SERVER = "SERVER"
KEYWORD_PORT = "PORT"
KEYWORD_COPYRIGHT = "COPYRIGHT"
KEYWORD_MAKE = "MAKE"
KEYWORD_MODEL = "MODEL"
KEYWORD_PREFIX = "PREFIX"
KEYWORD_BAND = "BAND"

# ZEROMQ COMMANDS
PORT_ODOMETRY = 6222
COMMAND_ODOMETERY = "ODOMETRY"
COMMAND_PING = "PING"
RESPONSE_ACK = "ACK"

# S3 INI
PROPERTY_SECTION_FILES = "FILES"
PROPERTY_SECTION_KEYS = "KEYS"
PROPERTY_IMAGES = "IMAGES"
PROPERTY_WEEDS_LOG = "WEEDS-LOG"
PROPERTY_KEY_IMAGES = "images.tar"
PROPERTY_KEY_WEEDS_LOG = "weeds-log"

#
# X M P P  R O O M S  A N D  J I D S
#
OLD_MESSAGE                          = 5000

PROPERTY_SECTION_XMPP                = "XMPP"
PROPERTY_SECTION_GENERAL             = "GENERAL"
PROPERTY_ROOT                        = "ROOT"
PROPERTY_PREFIX                      = "PREFIX"
PROPERTY_SUFFIX_META                 = "SUFFIX_META"
PROPERTY_DOMAIN_DNS                  = "DOMAIN"
PROPERTY_CONFERENCE_DNS              = "CONFERENCE_DNS"
PROPERTY_ROOM_ODOMETRY               = "ROOM_ODOMETRY"
PROPERTY_ROOM_TREATMENT              = "ROOM_TREATMENT"
PROPERTY_ROOM_SYSTEM                 = "ROOM_SYSTEM"
PROPERTY_SERVER                      = "SERVER"

PROPERTY_JID_ODOMETRY                = "JID_ODOMETRY"
PROPERTY_JID_RIO                     = "JID_RIO"
PROPERTY_JID_JETSON                  = "JID_JETSON"
PROPERTY_JID_JETSON_1                = "JID_JETSON1"
PROPERTY_JID_JETSON_2                = "JID_JETSON2"
PROPERTY_JID_CONSOLE                 = "JID_CONSOLE"
PROPERTY_JID_CLOUD                   = "JID_CLOUD"
PROPERTY_JID_CLOUD_1                 = "JID_CLOUD1"
PROPERTY_JID_CLOUD_2                 = "JID_CLOUD2"
PROPERTY_JID_CLOUD_3                 = "JID_CLOUD3"
PROPERTY_JID_CONTROL                 = "JID_CONTROL"
PROPERTY_POSITION                    = "POSITION"


PROPERTY_DEFAULT_PASSWORD            = "DEFAULT_PASSWORD"

PROPERTY_NICK_ODOMETRY               = "NICK_ODOMETRY"
PROPERTY_NICK_TREATMENT              = "NICK_TREATMENT"
PROPERTY_NICK_JETSON                 = "NICK_JETSON"
PROPERTY_NICK_JETSON_1               = "NICK_JETSON_1"
PROPERTY_NICK_JETSON_2               = "NICK_JETSON_2"
PROPERTY_NICK_CONSOLE                = "NICK_CONSOLE"
PROPERTY_NICK_CLOUD                  = "NICK_CLOUD"
PROPERTY_NICK_CLOUD_RIGHT            = "NICK_CLOUD_RIGHT"
PROPERTY_NICK_CLOUD_MIDDLE           = "NICK_CLOUD_MIDDLE"
PROPERTY_NICK_CLOUD_LEFT             = "NICK_CLOUD_LEFT"
PROPERTY_NICK_CONTROL                = "NICK_CONTROL"
PROPERTY_NICK_IMU                    = "NICK_IMU"
PROPERTY_MSG_TYPE_NORMAL             = "MSG_TYPE_NORMAL"
PROPERTY_MSG_TYPE_GROUPCHAT          = "MSG_TYPE_GROUPCHAT"

XMPP_PORT                            = 5222

PROPERTY_LEGO_A                      = "LEGO_A"
PROPERTY_LEGO_B                      = "LEGO_B"

PROPERTY_EMITTER_DIAG                = "DIAG-TYPE"
#
# J S O N  A N D  M E S S A G E S
#
JSON_ACCELERATION   = "acceleration"
JSON_ACTION         = "action"
JSON_DATA           = "data"
JSON_DEPTH          = "depth"
JSON_DIAG_MSG       = "diagnostic"
JSON_DISTANCE       = "distance"
JSON_EMITTER_TIER   = "tier"
JSON_EMITTER_POS    = "position"
JSON_EMITTER_NUMBER = "number"
JSON_EMITTER_DURATION = "duration"
JSON_GYRO           = "gyro"
JSON_IMAGE_NO       = "image_no"
JSON_NAME           = "name"
JSON_PLAN           = "plan"
JSON_SPEED          = "speed"
JSON_TIME           = "timestamp"
JSON_TOTAL_DISTANCE = "total_distance"
JSON_URL            = "url"
JSON_DIAG_RSLT      = "result"
JSON_DIAG_DETAIL    = "detail"
JSON_SOURCE         = "source"
JSON_LATITUDE       = "latitude"
JSON_LONGITUDE      = "longitude"
JSON_SEQUENCE       = "sequence"
JSON_OPERATION      = "operation"
JSON_PARAM_GSD      = "param-gsd"
JSON_POSITION       = "position"
JSON_PULSES         = "pulses"
JSON_PULSE_START    = "pulse_start"
JSON_PULSE_STOP     = "pulse_stop"
JSON_STATUS_CAMERA  = "status-camera"
JSON_STATUS_DAQ     = "status-daq"
JSON_STATUS_GPS     = "status-gps"
JSON_STATUS_INTEL   = "status-intel"
JSON_STATUS_ODOMETRY = "status-odometry"
JSON_STATUS_SYSTEM  = "status-system"
JSON_TARGET_LOCATION    = "location"
JSON_TARGET_DISTANCE    = "distance"
JSON_TYPE           = "type"


ENTITY_CAMERA       = "camera"
ENTITY_EMITTERS     = "emitters"
ENTITY_DAQ          = "daq"
ENTITY_SYSTEM       = "system"
ENTITY_GPS          = "gps"
ENTITY_INTEL        = "intel"

EMITTER_ALL         = "0"
EMITTER_NOT_SET     = "-1"

SOURCE_VIRTUAL      = "virtual"
SOURCE_PHYSICAL     = "physical"

MSG_RAW             = "raw"

ACTION_START        = "START"
ACTION_STOP         = "STOP"
ACTION_CONFIGURE    = "CONFIGURE"

DIAG_PASS   = "pass"
DIAG_FAIL   = "fail"

EMITTER_DIAGNOSTIC_WET = "wet"
EMITTER_DIAGNOSTIC_DRY = "dry"

class Diagnostic(Enum):
    FAIL = 0
    OK = 1

class Forward(Enum):
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1

class Treatment(Enum):
    RAW_IMAGE = 0
    PLAN = 1
    EMITTER_INSTRUCTIONS = 2
    CLASSIFICATION = 3
    UNKNOWN = 4

class Position(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

class SubsystemType(Enum):
    VIRTUAL = 0
    PHYSICAL = 1

class ImageType(Enum):
    RGB = 0
    DEPTH = 1
    BASLER_RAW = 2

class OdometryMessageType(Enum):
    DISTANCE = 0
    POSITION = 1
    UNKNOWN = 2

class Action(Enum):
    START = 0
    STOP = 1
    START_DIAG = 2
    DIAG_REPORT = 3
    PING = 4
    ACK = 5
    CURRENT = 6
    CONFIGURE = 7

class Operation(Enum):
    QUIESCENT = 0
    IMAGING = 1
    WEEDING = 2

class Orientation(Enum):
    UP = 0
    DOWN = 1
    UNKNOWN = 2

class OperationalStatus(Enum):
    OK = 0
    UNKNOWN = 1
    FAIL = 2

class XMPPStatus(Enum):
    CONNECTED = 0
    DISCONNECT_RETRY = 1
    DISCONNECT_FAIL = 2


class Status(Enum):
    QUIESCENT = 0
    RUNNING = 1
    EXIT_OK = 2
    EXIT_FATAL = 3

class Capture(Enum):
    DEPTH_RGB = 0
    DEPTH_DEPTH = 1
    IMU = 2
    RGB = 3
    IR = 4

class IntelCapture(Enum):
    RGBDEPTH = 0
    DEPTH = 1

class Side(Enum):
    RIGHT = 0
    LEFT = 1

class PositionWithEmitter(Enum):
    PRE = 0
    POST = 1

class ProcessResult(Enum):
    OK = 0
    EOF = 1
    NOTHING_FOUND = 2
    NOT_PROCESSED = 3
    INTERNAL_ERROR = 4

class Strategy(Enum):
    CARTOON = 0
    PROCESSED = 1

class Score(Enum):
    UNDEFINED = 0
    ROC = 1
    ACCURACY = 2

class Classification(Enum):
    CROP = 0
    WEED = 1




