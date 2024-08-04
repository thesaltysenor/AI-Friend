<!-- src/components/ImageGenerator.vue -->

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useImageService } from '@/services/imageService';

export default defineComponent({
    name: 'ImageGenerator',
    props: {
        aiPersonalityId: {
            type: Number,
            required: false
        }
    },
    setup(props, { emit }) {
        const { isGenerating, generatedImageUrl, generateImage, getImage } = useImageService();
        const imagePrompt = ref('');

        const handleGenerateImage = async () => {
            if (!imagePrompt.value) return;

            try {
                const promptId = await generateImage(imagePrompt.value, props.aiPersonalityId);
                const imageUrl = await getImage(promptId);
                emit('image-generated', imageUrl);
            } catch (error) {
                console.error('Error in image generation process:', error);
            }
        };

        return {
            imagePrompt,
            isGenerating,
            generatedImageUrl,
            handleGenerateImage
        };
    }
});
</script>