<template>
  <div class="rich-text-editor">
    <QuillEditor
      ref="quillEditor"
      :content="modelValue"
      :options="editorOptions"
      content-type="html"
      @update:content="handleUpdate"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])
const quillEditor = ref(null)

const editorOptions = {
  theme: 'snow',
  placeholder: 'Saisissez votre contenu...',
  modules: {
    toolbar: [
      [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      [{ 'font': [] }],
      [{ 'size': ['small', false, 'large', 'huge'] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'color': [] }, { 'background': [] }],
      [{ 'script': 'sub' }, { 'script': 'super' }],
      [{ 'list': 'ordered' }, { 'list': 'bullet' }],
      [{ 'indent': '-1' }, { 'indent': '+1' }],
      [{ 'align': [] }],
      ['blockquote', 'code-block'],
      ['link', 'image', 'video'],
      ['clean']
    ]
  }
}

const handleUpdate = (content) => {
  emit('update:modelValue', content)
}
</script>

<style scoped>
.rich-text-editor {
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  overflow: hidden;
}

.rich-text-editor :deep(.ql-container) {
  min-height: 200px;
  font-size: 1rem;
}

.rich-text-editor :deep(.ql-editor) {
  min-height: 200px;
}

.rich-text-editor :deep(.ql-editor p) {
  margin: 0.5rem 0;
}

.rich-text-editor :deep(.ql-editor h1) {
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem 0;
}

.rich-text-editor :deep(.ql-editor h2) {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0.75rem 0;
}

.rich-text-editor :deep(.ql-editor h3) {
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.rich-text-editor :deep(.ql-editor ul),
.rich-text-editor :deep(.ql-editor ol) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

.rich-text-editor :deep(.ql-editor img) {
  max-width: 100%;
  height: auto;
  margin: 1rem 0;
}

.rich-text-editor :deep(.ql-editor a) {
  color: #2563eb;
  text-decoration: underline;
}

.rich-text-editor :deep(.ql-snow) {
  border: none;
}

.rich-text-editor :deep(.ql-toolbar) {
  border: none;
  border-bottom: 1px solid #d1d5db;
  background-color: #f9fafb;
  padding: 0.5rem;
}
</style>
