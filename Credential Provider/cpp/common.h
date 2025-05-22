#pragma once
#include "helpers.h"

enum SAMPLE_FIELD_ID
{
    // Các field đang hoạt động
    SFI_TILEIMAGE = 0,
    SFI_LABEL = 1,
    SFI_LARGE_TEXT = 2,
    SFI_PASSWORD = 3,
    SFI_SUBMIT_BUTTON = 4,
    SFI_FACEID_BUTTON = 5,
    
    SFI_HIDECONTROLS_LINK = 6,
    SFI_DISPLAYNAME_TEXT = 7,
    SFI_LOGONSTATUS_TEXT = 8,
    
    
    // Các field không dùng (để dưới cùng)
    SFI_LAUNCHWINDOW_LINK = 9,
    SFI_FULLNAME_TEXT = 10,
    SFI_CHECKBOX = 11,
    SFI_EDIT_TEXT = 12,
    SFI_COMBOBOX = 13,
    
    SFI_NUM_FIELDS = 14  // Giữ nguyên tổng số field
};

struct FIELD_STATE_PAIR
{
    CREDENTIAL_PROVIDER_FIELD_STATE cpfs;
    CREDENTIAL_PROVIDER_FIELD_INTERACTIVE_STATE cpfis;
};

static const FIELD_STATE_PAIR s_rgFieldStatePairs[] =
{
    // Các field đang hoạt động
    { CPFS_DISPLAY_IN_BOTH,            CPFIS_NONE    },    // SFI_TILEIMAGE
    { CPFS_HIDDEN,                     CPFIS_NONE    },    // SFI_LABEL
    { CPFS_DISPLAY_IN_BOTH,            CPFIS_NONE    },    // SFI_LARGE_TEXT
    { CPFS_DISPLAY_IN_SELECTED_TILE,   CPFIS_FOCUSED },    // SFI_PASSWORD
    { CPFS_DISPLAY_IN_SELECTED_TILE,   CPFIS_NONE    },    // SFI_SUBMIT_BUTTON
    { CPFS_DISPLAY_IN_SELECTED_TILE,   CPFIS_NONE    },     // SFI_FACEID_BUTTON
    
    { CPFS_DISPLAY_IN_SELECTED_TILE,   CPFIS_NONE    },    // SFI_HIDECONTROLS_LINK
    { CPFS_DISPLAY_IN_SELECTED_TILE,   CPFIS_NONE    },    // SFI_DISPLAYNAME_TEXT
    { CPFS_DISPLAY_IN_SELECTED_TILE,   CPFIS_NONE    },    // SFI_LOGONSTATUS_TEXT
    
    
    // Các field không dùng
    { CPFS_HIDDEN,                     CPFIS_NONE    },    // SFI_LAUNCHWINDOW_LINK
    { CPFS_HIDDEN,                     CPFIS_NONE    },    // SFI_FULLNAME_TEXT
    { CPFS_HIDDEN,                     CPFIS_NONE    },    // SFI_CHECKBOX
    { CPFS_HIDDEN,                     CPFIS_NONE    },    // SFI_EDIT_TEXT
    { CPFS_HIDDEN,                     CPFIS_NONE    }     // SFI_COMBOBOX
    
    
};

static const CREDENTIAL_PROVIDER_FIELD_DESCRIPTOR s_rgCredProvFieldDescriptors[] =
{
    // Các field đang hoạt động
    { SFI_TILEIMAGE,         CPFT_TILE_IMAGE,    L"Image",                      CPFG_CREDENTIAL_PROVIDER_LOGO  },
    { SFI_LABEL,             CPFT_SMALL_TEXT,    L"Tooltip",                    CPFG_CREDENTIAL_PROVIDER_LABEL },
    { SFI_LARGE_TEXT,        CPFT_LARGE_TEXT,    L"Sample Credential Provider"                                 },
    { SFI_PASSWORD,          CPFT_PASSWORD_TEXT, L"Password text"                                              },
    { SFI_SUBMIT_BUTTON,     CPFT_SUBMIT_BUTTON, L"Submit"                                                     },
    { SFI_FACEID_BUTTON,     CPFT_COMMAND_LINK,  L"Face ID"                                                    },
    
    { SFI_HIDECONTROLS_LINK, CPFT_COMMAND_LINK,  L"Hide additional controls"                                   },
    { SFI_DISPLAYNAME_TEXT,  CPFT_SMALL_TEXT,    L"Display name: "                                             },
    { SFI_LOGONSTATUS_TEXT,  CPFT_SMALL_TEXT,    L"Logon status: "                                             },
    
    
    // Các field không dùng
    { SFI_LAUNCHWINDOW_LINK, CPFT_COMMAND_LINK,  L"Launch helper window"                                       },
    { SFI_FULLNAME_TEXT,     CPFT_SMALL_TEXT,    L"Full name: "                                                },
    { SFI_CHECKBOX,          CPFT_CHECKBOX,      L"Checkbox"                                                   },
    { SFI_EDIT_TEXT,         CPFT_EDIT_TEXT,     L"Edit text"                                                  },
    { SFI_COMBOBOX,          CPFT_COMBOBOX,      L"Combobox"                                                   }
    
    
};

static const PWSTR s_rgComboBoxStrings[] =
{
    L"First",
    L"Second",
    L"Third",
};
