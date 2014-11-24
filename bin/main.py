#!/usr/bin/env python3

from common import load_obj, edit_cls, expr, expr_type, expr_type_multi


def main():
    load_obj()

    edit = edit_cls('NemesisApplication')
    edit.prepare_after_prologue('onCreate')
    edit.add_invoke_entry('NemesisApp_onOnCreate', 'p0')

    edit.prepare_after_invoke_init('AssetFinder')
    edit.add_invoke_entry('AssetFinder_onInit', edit.vars[0])
    edit.save()

    edit = edit_cls('NemesisActivity')
    edit.prepare_after_prologue('onCreate')
    edit.add_invoke_entry('NemesisActivity_onOnCreate', 'p0')
    edit.prepare_after_prologue('onPause')
    edit.add_invoke_entry('NemesisActivity_onOnPause', 'p0')
    edit.prepare_after_prologue('onResume')
    edit.add_invoke_entry('NemesisActivity_onOnResume', 'p0')
    edit.save()

    edit = edit_cls('NemesisWorld')
    edit.mod_field_def('subActivityManager', 'public')
    edit.find_line(r' new-array ([vp]\d+), ([vp]\d+), \[%s' % expr_type('$BaseSubActivity'))
    edit.find_line(r' return-void', where='down')
    edit.prepare_to_insert_before(True)
    edit.add_line(' move-object/from16 v0, p0')
    edit.add_invoke_entry('NemesisWorld_onInit', 'v0')

    edit.find_line(r' const-class (v\d+), %s' % expr_type('$Space2FaceActivity'))
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('shouldSkipIntro')
    edit.add_line(' move-result %s' % edit.vars[0])
    edit.add_line(' if-nez %s, :mod_0' % edit.vars[0])
    edit.curr += 3
    edit.split_lines()
    edit.curr += 1
    edit.prepare_to_insert()
    edit.add_line(' :mod_0')

    edit.prepare_after_invoke_init('MenuControllerImpl')
    edit.add_invoke_entry('MenuController_onInit', edit.vars[0])
    edit.save()

    edit = edit_cls('SubActivityManager')
    edit.mod_field_def('skin', 'public')
    edit.prepare_after_prologue('init')
    edit.add_invoke_entry('SubActivityManager_onInit', 'p2')
    edit.save()

    edit = edit_cls('SubActivityApplicationListener')
    edit.find_method_def('create')
    edit.find_line(r' return-void', where='down')
    edit.prepare_to_insert_before(True)
    edit.add_invoke_entry('SubActivityApplicationLisener_onCreated')
    edit.save()

    edit = edit_cls('MenuTabId')
    edit.add_enum('MOD_ABOUT')
    edit.add_enum('MOD_ITEMS')
    edit.prepare_after_prologue('getText2')
    edit.add_invoke_entry('MenuTabId_onToString', 'p0', 'v0')
    edit.add_ret_if_result(True, 'result')
    edit.save()

    edit = edit_cls('MenuTopWidget')
    edit.find_line(r' invoke-static {}, %s->values\(\)\[%s' % tuple(expr_type_multi('$MenuTabId', '$MenuTabId')))
    edit.comment_line()
    edit.add_invoke_entry('MenuTopWidget_getTabs')
    edit.save()

    edit = edit_cls('MenuControllerImpl')
    edit.mod_field_def('subActivityManager', 'public')
    edit.prepare_after_prologue('selectTab')
    edit.add_invoke_entry('MenuControllerImpl_onSelectTab', 'p0, p1', 'v0')
    edit.add_ret_if_result(True)
    edit.save()

    edit = edit_cls('AvatarPlayerStatusBar_OpsButtonListener')
    edit.find_line(' const-class (v\d+), %s' % expr_type('$ItemsActivity'))
    edit.comment_line()
    edit.add_invoke_entry('MenuShowBtn_onClick')
    edit.add_line(' move-result-object %s' % edit.vars[0])
    edit.save()
    
    edit = edit_cls('AvatarPlayerStatusBar_AvatarListener')
    edit.prepare_after_prologue('clicked')
    edit.add_invoke_entry('Mod_ShowAgentTab', '', 'v0')
    edit.add_ret_if_result(False)
    edit.save()
    
    edit = edit_cls('AssetFinder')
    edit.find_line(r' const-string/jumbo v\d+, "\{"')
    edit.find_prologue(where="up")
    edit.prepare_to_insert(2)
    edit.add_invoke_entry('AssetFinder_onGetAssetPath', 'p1', 'v0')
    edit.add_ret_if_result(True, 'result')

    edit.mod_field_def('screenDensity', 'public')
    edit.save()

    edit = edit_cls('GroupDrawer')
    edit.find_line(r' invoke-interface \{.+?\}, %s->a\(Lcom/badlogic/gdx/math/Matrix4;.+' % expr_type('$Drawer'))
    edit.find_prologue(where='up')
    edit.prepare_to_insert(2)
    edit.add_invoke_entry('shouldDrawScannerObject', '', 'v0')
    edit.add_ret_if_result(False)
    edit.save()

    edit = edit_cls('PortalInfoDialog')
    edit.mod_field_def('portalComponent', 'public')

    edit.find_line(r' .+"Owner: "')
    edit.find_line(
        r' return-object ([pv]\d+)',
        where='down')
    tab = edit.vars[0]
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('PortalInfoDialog_onStatsTableCreated', 'p0, %s' % tab)

    edit.prepare_after_prologue('onPlayerLocationChanged')
    edit.add_invoke_entry('PortalInfoDialog_onPlayerLocationChanged')
    edit.save()

    edit = edit_cls('PortalDialogMode')
    edit.find_line(r' const.*? ([pv]\d+), 0x3f40')
    edit.prepare_to_insert()
    edit.add_invoke_entry('PortalInfoDialog_getOpenDelay', edit.vars[0], edit.vars[0])
    edit.save()

    edit = edit_cls('NoPortalsScannerState')
    edit.find_line(r' const/4 v1, 0x1');
    edit.comment_line()
    edit.add_invoke_entry('ShouldShowPortalVectors', '', 'v1')
    edit.save()

    edit = edit_cls('ScannerStateManager')
    edit.find_line(r'.method public constructor \<init\>\(.*') # instance constructor
    edit.find_line(r' return-void', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('ScannerStateManager_onInit', 'p0')

    edit.mod_method_def('togglePortalVectors', 'public')
    edit.save()

    edit = edit_cls('ZoomInMode')
    edit.find_method_def('onEnter')
    edit.find_line(r' iput-object [pv]\d+, p0, %s->h.+' % expr_type('$ZoomInMode'))
    edit.prepare_to_insert()
    edit.add_invoke_entry('ZoomInMode_shouldZoomIn', '', 'v0')
    edit.add_ret_if_result(False)
    edit.save()

    edit = edit_cls('ClientFeatureKnobBundle')
    edit.find_method_def('getEnableInviteNag')
    edit.find_line(r' return (v\d+)', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('isInviteNagEnabled', edit.vars[0], edit.vars[0])
    edit.save()

    edit = edit_cls('HackController')
    edit.find_line(r'.*method private a\(.*;Z\)V')
    edit.find_prologue(where="down")
    edit.prepare_to_insert()
    edit.add_invoke_entry('HackController_shouldShowAnimation', '', 'v0')
    edit.add_ret_if_result(False)
    edit.save()
    
    edit = edit_cls('HackAnimationStage')
    edit.find_method_def('getTotalTime')
    edit.find_line(r' return ([pv]\d+)')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('HackAnimationStage_getTotalTime', edit.vars[0], edit.vars[0])
    edit.save()

    #portal particles
    edit = edit_cls('PortalParticleRender')
    edit.find_line(' invoke-interface \{v1\}, %s->getLevel\(\)I' % expr('$Portal', regex=True))
    edit.prepare_to_insert_before()
    edit.add_line(' move-object v14, v1')
    edit.find_line(' invoke-direct/range \{v1 .. v9\}, %s' % expr('$PortalParticleParameters->init()', regex=True))
    edit.prepare_to_insert()
    edit.add_line(' iput-object v14, v1, %s->portalComponent:%s' % (expr_type('$PortalParticleParameters'), expr_type('$Portal')))

    edit.find_line(' check-cast v0, %s' % expr_type('$PortalParticleParameters'))
    edit.prepare_to_insert()
    edit.add_invoke_entry('PortalParticleRender_tweakParameters', 'v0', 'v0')
    edit.find_line(' check-cast v0, %s' % expr_type('$PortalParticleParameters'), where='down')
    edit.prepare_to_insert()
    edit.add_invoke_entry('PortalParticleRender_tweakParameters', 'v0', 'v0')
    edit.save()

    edit = edit_cls('PortalParticleParameters')
    edit.find_class_def()
    edit.prepare_to_insert()
    edit.add_line(' .field public portalComponent:%s' % expr_type('$Portal'))
    edit.mod_class_def('public')
    edit.mod_field_def('renderer', 'public')
    edit.mod_field_def('latlng', 'public')
    edit.mod_field_def('color', 'public')
    edit.save()

    #disable xm flow
    edit = edit_cls('ParticleEnergyGlobVisuals')
    edit.find_line(r' const-string/jumbo v0, "u_timeSec"')
    edit.find_line(r' .*Lcom/badlogic/gdx/graphics/glutils/ShaderProgram;->setUniformf.*', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('ParticleEnergyGlobVisuals_getTimeSec', 'v1', 'v1')
    edit.save()
    
    #disable shield animation
    edit = edit_cls('ShieldShader')
    edit.find_line(r' const-string/jumbo ([pv]\d+), "u_rampTargetInvWidth"')
    edit.find_line(r' .*Lcom/badlogic/gdx/graphics/glutils/ShaderProgram;->setUniformf.*', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('ShieldShader_getRampTargetInvWidthX', 'v0', 'v0')
    edit.add_invoke_entry('ShieldShader_getRampTargetInvWidthY', 'v4', 'v4')
    edit.save()

    #stop inventory item rotation
    edit = edit_cls('InventoryItemRenderer')
    edit.prepare_after_prologue('rotate')
    edit.add_invoke_entry('InventoryItemRenderer_shouldRotate', ret='v0')
    edit.add_ret_if_result(False, 'result')
    edit.save()

    #simplify inventory item rendering
    edit = edit_cls('InventoryItemRenderer')
    edit.find_line(' const-string/jumbo v1, "u_altColor"')
    edit.find_line(' invoke-virtual .*Lcom/badlogic/gdx/graphics/glutils/ShaderProgram;', where='up')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('InventoryItemRenderer_simplifyItems', ret='v2')
    edit.add_line(' if-nez v2, :skip_item_shader')
    edit.find_line('.*Lcom/badlogic/gdx/graphics/glutils/ShaderProgram;->end.*', where='down')
    edit.prepare_to_insert()
    edit.add_line(' :skip_item_shader')
    edit.save()

    edit = edit_cls('BaseItemDetailsUiCreator')
    edit.find_method_def('addRarityLabel')
    edit.find_line(r' invoke-virtual \{([pv]\d+)\}, %s->a().*' % (expr('$ItemRarity')), where='down')
#    edit.find_line(r' return-void', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('BaseItemDetailsUiCreator_OnAddRarityLabel', 'p1, p2, p3, v0')
    edit.find_method_def('addActionButtons')
    edit.find_line(r' return-void', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('BaseItemDetailsUiCreator_OnAddActionButtons', 'p1, p2, p3')
    edit.save()

    edit = edit_cls('PowerCubeDetailsUiCreator')
    edit.find_method_def('addActionButtons')
    edit.find_line(r' invoke-super .*', where='down')
    edit.prepare_to_insert()
    edit.add_invoke_entry('PowerCubeDetailsUiCreator_onActionButtonsTableCreated', 'p1')
    edit.save()

    #modify shader code before compiling it
    edit = edit_cls('ShaderUtils')
    edit.find_line(r' new-instance ([pv]\d+), Lcom/badlogic/gdx/graphics/glutils/ShaderProgram;')
    shaderReg = edit.vars[0]
    edit.comment_line()
    edit.find_line(r' invoke-direct \{.*\}, Lcom/badlogic/gdx/graphics/glutils/ShaderProgram;-><init>\(Ljava/lang/String;Ljava/lang/String;\)V', where='down')
    edit.comment_line()
    edit.prepare_to_insert()
    edit.add_invoke_entry('ShaderUtils_compileShader', 'p0, p1, p2', shaderReg)
    edit.save()

    edit = edit_cls('CommStreamAdapter')
    edit.prepare_after_prologue('getView')
    edit.find_line(r' sget-object ([pv]\d+), %s->a:%s' % (expr('$CommStreamAdapter'), expr('$SimpleDateFormat')))
    edit.comment_line()
    edit.add_invoke_entry('CommsAdapter_getDateFormat', '', edit.vars[0])
    edit.save()

    #remove recycle animation
    edit = edit_cls('ItemActionHandler')
    edit.find_method_def('recycle')
    edit.find_line(' \.locals 4', where='down')
    edit.replace_in_line('4', '5')
    edit.find_line(' const-wide/16 v2, 0x4b0', where='down')
    edit.prepare_to_insert()
    edit.add_invoke_entry('ItemActionHandler_recycleAnimationsEnabled', ret='v4')
    edit.add_line(' if-nez v4, :lbl_recycle_delay');
    edit.add_line(' const-wide/16 v2, 0x0')
    edit.add_line(' :lbl_recycle_delay')
    edit.save()

    # disable vibration
    edit = edit_cls('AndroidInput')
    edit.find_method_def('vibrateInt')
    edit.find_line(' \.locals 3', where='down')
    edit.replace_in_line('3', '4')
    edit.find_line('.*invoke-virtual \{.*\}, Landroid/os/Vibrator;->vibrate\(J\)V.*', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('vibrationEnabled', ret='v3')
    edit.add_line(' if-eqz v3, :lbl_vibration_disabled')
    edit.curr += 2;
    edit.add_line(' :lbl_vibration_disabled')
    edit.save()

    # change gps lock timeout
#    edit = edit_cls('GpsSensor')
#    edit.find_line(' .*Landroid/os/Handler;->postDelayed.*')
#    edit.prepare_to_insert_before()
#    edit.add_invoke_entry('GpsSensor_lockTimeout', ret='v2')
#    edit.save()

    #change order of buttons in round menu
    edit = edit_cls('ScannerTouchHandler')
    
    edit.find_line(' invoke-direct/range \{v0 \.\. v7\}, (.+)$')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('ScannerTouchHandler_shouldSwapTouchMenuButtons', ret='v11')
    edit.add_line(' if-eqz v11, :noswap')
    edit.add_line(' move-object v11, v3')
    edit.add_line(' move-object v3, v6')
    edit.add_line(' move-object v6, v11')
    edit.add_line(' :noswap')
    
    edit.prepare_after_prologue('touchDown')
    edit.add_invoke_entry('ScannerTouchHandler_onTouchDown', 'p1, p2, p3')
    edit.save()

    #change format for AP and XM in COMM
    edit = edit_cls('CommPlayerListener')
    edit.find_line(r'(.+)%d XM(.+)$')
    edit.replace_in_line('%d', '%,d')
    edit.find_line(r'(.+)%d AP(.+)$')
    edit.replace_in_line('%d', '%,d')
    edit.save()

    edit = edit_cls('ScannerActivity')
    edit.prepare_after_prologue('updateState')
    edit.add_invoke_entry('ScannerActivity_onUpdateState', 'p0')
    edit.save()

    # privacy
    edit = edit_cls('AvatarPlayerStatusBar')
    edit.find_line(' invoke-interface {v0, v1}, %s->a\(Ljava/lang/String;\)V' % expr('$PlayerListener'))
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('isPrivacyEnabled', ret='v5')
    edit.add_line(' if-eqz v5, :lbl_privacy_disabled')
    edit.add_line(' const-string/jumbo v1, ""')
    edit.add_line(' :lbl_privacy_disabled')
    
    edit.mod_field_def('stage', 'public')
    edit.mod_field_def('skin', 'public')
    edit.mod_field_def('contentGroup', 'public')

    edit.find_method_def('createUi')
    edit.find_line(' new-instance v0, %s' % expr('$Group'))
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('AvatarPlayerStatusBar_onCreateUi', 'p0')

    edit.find_line(r' invoke-virtual \{p2, ([pv]\d+)\}, %s->addActor\(%s\)V' % (expr('$Stage'), expr('$Actor')))
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('AvatarPlayerStatusBar_onStageAddActor', edit.vars[0])
    edit.find_line(r' invoke-virtual \{p2, ([pv]\d+)\}, %s->addActor\(%s\)V' % (expr('$Stage'), expr('$Actor')))
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('AvatarPlayerStatusBar_onStageAddActor', edit.vars[0])
    edit.find_line(r' invoke-virtual \{p2, ([pv]\d+)\}, %s->addActor\(%s\)V' % (expr('$Stage'), expr('$Actor')))
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('AvatarPlayerStatusBar_onStageAddActor', edit.vars[0])

#    edit.prepare_to_insert()
    edit.find_line(r' return-void', where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('AvatarPlayerStatusBar_onCreatedUi', 'p0')
    edit.save()

    edit = edit_cls('TutorialDialogNextListener')
    edit.mod_class_def('public')
    edit.mod_method_def('init', 'public')
    edit.save()

    edit = edit_cls('TutorialDialog')
    edit.find_method_def('createUi')
    edit.find_line(r' new-instance v5, %s' % expr('$Table'), where='down')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('TutorialDialog_onCreateUi', 'p0, v4')
    edit.save()

    edit = edit_cls('com.nianticproject.ingress.common.missions.tutorial.TutorialDialog$Style')
    edit.find_line(r' iput v0, p0, Lcom/nianticproject/ingress/common/missions/tutorial/TutorialDialog\$Style;->padTop:I')
    edit.prepare_to_insert_before()
    edit.add_invoke_entry('TutorialDialogStyle_getPadTop', 'v0', 'v0')
    edit.save()

    edit = edit_cls('ActionButton')
    edit.find_method_def('init')
    edit.find_line(r' const/high16 v1, 0x3f80')
    edit.prepare_to_insert()
    edit.add_invoke_entry('ActionButton_getScale', 'v1', 'v1')
    edit.save()

if __name__ == '__main__':
    main()
