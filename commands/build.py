#    @property
#    def short_desc(self):
#        return self.db.short_desc
#    
#    @short_desc.setter
#    def short_desc(self, value):
#        if not value:
#            pass
#        else:
#            self.db.short_desc = str(value)

from commands.command import MuxCommand
from evennia import CmdSet, utils
from utils.flags_handler import FlagsHandler

class BuildCmdSet(CmdSet):

    key = "build_cmdset"
    priority = 2

    def at_cmdset_creation(self):
        "Populate CmdSet"
        self.add(CmdFlag())
        #self.add(CmdSize())

class CmdFlag(MuxCommand):
    """
    This is the command used to apply room's FLAGS.
    Flags are picked from the following list:
    
      * is_indoor
      * is_dark
      * is_safe
      * has_road
      * no_magic
      * no_teleport
      * no_summon
      * is_silent
      * no_range
      * is_water
      * is_air
      * no_quit
        
    Usage:
      @flag[/switches] <obj> = <flag>
    
    Switches:
      del = remove flag
    """
    
    key = "@flag"
    locks = "cmd:perm(flag) or cmd:perm(Builders)"
    help_category = "Building"
    
    def func(self):
        "Implement the Flag command"
        flags = (
            "is_indoor",
            "is_dark",
            "is_safe",
            "has_road",
            "no_magic",
            "no_teleport",
            "no_summon",
            "is_silent",
            "no_range",
            "is_water",
            "is_air",
            "no_quit"
            )
        if not self.args:
            self.caller.msg("Usage: @flag[/switches] <obj> = <flag>")
            return
        if "del" in self.switches:
            # remove one flag
            obj = self.caller.search(self.lhs, global_search=True)
            if not obj:
                return
            if self.rhs:
                # remove individual tag
                flag = self.rhs
                handler = FlagsHandler(obj)
                handler.remove(flag)
                string = "Removed flag '%s' from %s." % (flag, obj)
            else:
                # no tag specified, send error message
                string = "You need to provide a flag to be deleted." % obj
            self.caller.msg(string)
            return
        if self.rhs:
            # = is found, so we are on the form obj = tag
            obj = self.caller.search(self.lhs, global_search=True)
            if not obj:
                return
            flag = self.rhs
            handler = FlagsHandler(obj)
            if flag in flags:
                # create the tag
                handler.add(flag)
                string = "Added flag '%s' to %s." % (flag, obj)
                self.caller.msg(string)
            else:
                string = "'%s' is not a possible flag. You may add it as a tag (see help @tag)" % flag
                self.caller.msg(string)
        else:
            # no '=' found - list tags on object
            obj = self.caller.search(self.args, global_search=True)
            if not obj:
                return
            handler = FlagsHandler(obj)
            string = handler.lists()
            self.caller.msg(string)

#class CmdSize(MuxCommand):
#    """
#    used to set/change room size
#    """
#    
#    key = '@size'
#    locks = 'cmd:perm(size) or cmd:perm(Builders)'
#    help_category = 'Building'
#    
#    def func(self):
#        """Implement the size command"""
#        if not self.args:
#            self.caller.msg("Usage: @size <obj> <small/medium/size>
