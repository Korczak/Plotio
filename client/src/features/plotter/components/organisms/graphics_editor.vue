<template>
  <div>
    <card-dialog
      v-model="dialog"
      title="Edytor grafik"
      width="100%"
      max-width="100%"
      persistent
    >
      <v-row>
        <v-col class="mt-3" cols="4">
          <image-settings @onChange="onChange"></image-settings>
        </v-col>
        <v-col cols="8">
          <image-preview
            ref="image-preview"
            width="600px"
            height="400px"
          ></image-preview>
        </v-col>
      </v-row>
      <template v-slot:actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save">Zatwierdź</v-btn>
      </template>
    </card-dialog>
  </div>
</template>

<script lang="ts">
import { Component, VModel, Vue } from "vue-property-decorator";
import SaveRestoreProjectButtons from "../molecules/save_restore_project_buttons.vue";
import ImageSettings from "../molecules/image_settings.vue";
import { approveImageImageApproveImagePost } from "@/api";
import ImagePreview from "../molecules/image_preview.vue";

@Component({
  components: { SaveRestoreProjectButtons, ImageSettings, ImagePreview },
})
export default class GraphicsEditor extends Vue {
  @VModel({ type: Boolean }) dialog: boolean | undefined;

  async save() {
    await approveImageImageApproveImagePost();
    this.dialog = false;
  }

  onChange() {
    const imagePreview = this.$refs["image-preview"] as ImagePreview;

    imagePreview.reloadImage();
  }
}
</script>

<style scoped></style>
