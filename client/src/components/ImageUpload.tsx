import { useCallback, useState } from "react";
import { Upload, X, Loader2, Library as LibraryIcon, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import type { ClothingItem } from "@shared/schema";
import { detectClothingType, quickDetectTypeFromFilename } from "@/lib/mlApi";
import { uploadImageToFirebase, isFirebaseConfigured } from "@/lib/firebase";

interface ImageUploadProps {
  onImagesChange: (items: ClothingItem[]) => void;
  onOpenLibrary: () => void;
  maxImages?: number;
}

export function ImageUpload({ onImagesChange, onOpenLibrary, maxImages = 8 }: ImageUploadProps) {
  const [items, setItems] = useState<ClothingItem[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [detectingTypes, setDetectingTypes] = useState<Set<string>>(new Set());
  const [saveToLibrary, setSaveToLibrary] = useState(true);
  const [uploadingToFirebase, setUploadingToFirebase] = useState<Set<string>>(new Set());
  const [firebaseConfigured] = useState(isFirebaseConfigured());

  const handleFileSelect = useCallback(
    async (files: FileList | null) => {
      if (!files) return;

      const remainingSlots = maxImages - items.length;

      const filesToProcess = Array.from(files).slice(0, remainingSlots);

      for (const file of filesToProcess) {
        if (file.type.startsWith("image/")) {
          const reader = new FileReader();
          reader.onload = async (e) => {
            const imageUrl = e.target?.result as string;
            const newItemId = Math.random().toString(36).substr(2, 9);
            
            // Quick filename check first
            let detectedType = quickDetectTypeFromFilename(file.name);
            
            // Create item with initial type
            const newItem: ClothingItem = {
              id: newItemId,
              imageUrl,
              type: detectedType || undefined,
              detectedType: detectedType || undefined,
            };
            
            setItems((prev) => {
              const updated = [...prev, newItem];
              onImagesChange(updated);
              return updated;
            });

            // Upload to Firebase if enabled and configured
            if (saveToLibrary && firebaseConfigured) {
              setUploadingToFirebase((prev) => new Set(prev).add(newItemId));
              
              try {
                const firebaseUrl = await uploadImageToFirebase(file);
                console.log('Image uploaded to Firebase:', firebaseUrl);
                
                // Update item with Firebase URL
                setItems((prev) => {
                  const updated = prev.map((item) =>
                    item.id === newItemId
                      ? { ...item, imageUrl: firebaseUrl }
                      : item
                  );
                  onImagesChange(updated);
                  return updated;
                });
              } catch (error) {
                console.error('Failed to upload to Firebase:', error);
                // Continue with local base64 URL
              } finally {
                setUploadingToFirebase((prev) => {
                  const next = new Set(prev);
                  next.delete(newItemId);
                  return next;
                });
              }
            }

            // If we couldn't detect from filename, use ML
            if (!detectedType) {
              setDetectingTypes((prev) => new Set(prev).add(newItemId));
              
              try {
                const mlResult = await detectClothingType(file);
                const mlType = mlResult.predicted_type;
                
                setItems((prev) => {
                  const updated = prev.map((item) =>
                    item.id === newItemId
                      ? { ...item, type: mlType, detectedType: mlType }
                      : item
                  );
                  onImagesChange(updated);
                  return updated;
                });
              } catch (error) {
                console.error('ML type detection failed:', error);
              } finally {
                setDetectingTypes((prev) => {
                  const next = new Set(prev);
                  next.delete(newItemId);
                  return next;
                });
              }
            }
          };
          reader.readAsDataURL(file);
        }
      }
    },
    [items.length, maxImages, onImagesChange, saveToLibrary, firebaseConfigured]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      handleFileSelect(e.dataTransfer.files);
    },
    [handleFileSelect]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const removeItem = (id: string) => {
    setItems((prev) => {
      const updated = prev.filter((item) => item.id !== id);
      onImagesChange(updated);
      return updated;
    });
  };

  return (
    <div className="space-y-6">
      {/* Library and Settings Bar */}
      <div className="flex items-center justify-between gap-4 p-4 rounded-lg border bg-card">
        <div className="flex items-center space-x-2">
          <Switch
            id="save-library"
            checked={saveToLibrary}
            onCheckedChange={setSaveToLibrary}
            disabled={!firebaseConfigured}
          />
          <Label htmlFor="save-library" className="text-sm">
            {firebaseConfigured ? (
              <>Save to library <Save className="inline h-3 w-3 ml-1" /></>
            ) : (
              <>Library (Configure Firebase)</>
            )}
          </Label>
        </div>
        
        <Button
          variant="outline"
          onClick={onOpenLibrary}
          className="gap-2"
        >
          <LibraryIcon className="h-4 w-4" />
          My Library
        </Button>
      </div>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`relative min-h-64 rounded-2xl border-2 border-dashed transition-colors ${
          isDragging
            ? "border-primary bg-primary/5"
            : "border-border hover:border-primary/50"
        }`}
        data-testid="dropzone-upload"
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept="image/*"
          multiple
          onChange={(e) => handleFileSelect(e.target.files)}
        />
        <label
          htmlFor="file-upload"
          className="flex min-h-64 cursor-pointer flex-col items-center justify-center p-8 text-center"
        >
          <Upload className="mb-4 h-12 w-12 text-muted-foreground" />
          <p className="mb-2 text-lg font-semibold" data-testid="text-upload-title">
            Drop your clothing photos here
          </p>
          <p className="text-sm text-muted-foreground">
            or click to browse ({items.length}/{maxImages} images)
          </p>
        </label>
      </div>

      {items.length > 0 && (
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
          {items.map((item) => (
            <Card key={item.id} className="group relative aspect-square overflow-hidden p-0">
              <img
                src={item.imageUrl}
                alt="Clothing item"
                className="h-full w-full object-cover"
                data-testid={`image-clothing-${item.id}`}
              />
              
              {/* Upload Status Badge */}
              {uploadingToFirebase.has(item.id) && (
                <div className="absolute top-2 left-2 rounded-md bg-blue-600 px-2 py-1 text-xs text-white backdrop-blur-sm flex items-center gap-1">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  Saving...
                </div>
              )}
              
              {/* ML Type Badge */}
              {item.detectedType && (
                <div className="absolute bottom-2 left-2 rounded-md bg-black/70 px-2 py-1 text-xs text-white backdrop-blur-sm">
                  {detectingTypes.has(item.id) ? (
                    <span className="flex items-center gap-1">
                      <Loader2 className="h-3 w-3 animate-spin" />
                      Detecting...
                    </span>
                  ) : (
                    <span className="capitalize">{item.detectedType}</span>
                  )}
                </div>
              )}
              
              <Button
                variant="destructive"
                size="icon"
                className="absolute right-2 top-2 h-8 w-8 shadow-lg"
                onClick={() => removeItem(item.id)}
                data-testid={`button-remove-${item.id}`}
              >
                <X className="h-4 w-4" />
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
